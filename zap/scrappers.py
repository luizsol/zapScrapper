import logging
from multiprocessing import Pool
from random import shuffle
from threading import Thread
import time
import warnings

import mongoengine

from . import api
from .. import models

MAXIMUM_EAGERNESS = None
HIGH_EAGERNESS = 1
MEDIUM_EAGERNESS = 2
LOW_EAGERNESS = 3

_package_worker = None

logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")


class General(object):
    """Updates the states and regions list."""

    def __init__(self, states=None, processes=5, eagerness=MEDIUM_EAGERNESS):
        if states is None:
            self.states = list(api.get_states_list().keys())
            shuffle(self.states)
        else:
            self.states = states

        self.eagerness = eagerness
        self.processes = processes

    def _list_neighborhoods(self, state):
        print(f'Scouting locations in the state {state}')

        results = api.get_neighborhoods_list(
            state=state, region=None, raw=False, lite=True,
            c2_delay_df=self.eagerness, norm_delay_m=None, norm_delay_sd=None)

        models.ZapFetchJob.objects.insert(
            [models.ZapFetchJob(**{**result, 'page': 0}) for result in results]
        )

        print(f'Done scouting locations in the state {state}')

    def run(self):
        processes = min(self.processes, len(self.states))

        if processes == 0:
            logger.error('No states to list.')
            return

        print(f'Spawning {self.processes} processes for class General.')

        p = Pool(processes)
        return p.map_async(self._list_neighborhoods, self.states)


class Scout(object):
    """Retrieve search results details."""

    def __init__(self, fetch_jobs=None, processes=5,
                 eagerness=MEDIUM_EAGERNESS):
        self.processes = processes
        self.eagerness = eagerness
        if fetch_jobs is None:
            self.fetch_jobs = list(models.ZapFetchJob.objects.filter(page=0))
            shuffle(self.fetch_jobs)
        else:
            self.fetch_jobs = fetch_jobs

    def _add_location_search_pages(self, fetch_job):
        """Retrieve search results details.

        Args:
            fetch_job: models.ZapFetchJob
        """
        print(f'Fetching data from state {fetch_job.state} and neighborhood'
              f' {fetch_job.neighborhood}.')

        number_of_pages, _, parsed_results = api.get_search_results(
            max_price=2147483647, neighborhood=fetch_job.neighborhood,
            city_side='', city='', state=fetch_job.state, page=1,
            get_details=True, raw=False, c2_delay_df=self.eagerness,
            norm_delay_m=None, norm_delay_sd=None
        )

        print(f'{number_of_pages} pages for state {fetch_job.state}'
              f' and neighborhood {fetch_job.neighborhood}.')

        if number_of_pages == 0 or len(parsed_results) == 0:
            return None

        for result in parsed_results.values():
            if len(result['features']) > 0:
                features = [models.RealEstateFeature(
                    name=feature) for feature in result['features']]

                result['features'] = features

            models.RealEstate(**result).save()

        # not working :(
        # models.RealEstate.objects.insert([
        #     models.RealEstate(**result) for result in parsed_results
        # ])

        fetch_job.update(page=1, in_progress=True, fetched=True)

        if number_of_pages == 1:
            return

        for i in range(2, number_of_pages + 1):
            models.ZapFetchJob(
                fetched=False,
                in_progress=False,
                neighborhood=fetch_job.neighborhood,
                page=i,
                state=fetch_job.state,
            ).save()

        # models.ZapFetchJob.objects.insert([models.ZapFetchJob(
        #         fetched=False,
        #         in_progress=False,
        #         neighborhood=fetch_job.neighborhood,
        #         page=i,
        #         state=fetch_job.state,
        #     ) for i in range(2, number_of_pages + 1)])

    def run(self):
        processes = min(self.processes, len(self.fetch_jobs))

        if processes == 0:
            logger.error('No fetch jobs to detail.')
            return None

        print(f'Spawning {self.processes} Scout processes.')

        p = Pool(processes)
        return p.map_async(self._add_location_search_pages, self.fetch_jobs)



class Worker(object):
    _running = False

    def __init__(self, processes=5, eagerness=MEDIUM_EAGERNESS):
        self.processes = processes
        self.eagerness = eagerness

    def work(self, worker_job):
        """Retrieve search results details.

        Args:
            worker_job: models.ZapFetchJob
        """
        print(f'Working on job {worker_job}.')

        worker_job.update(in_progress=True)

        _, _, parsed_results = api.get_search_results(
            max_price=2147483647, neighborhood=worker_job.neighborhood,
            city_side='', city='', state=worker_job.state,
            page=worker_job.page, get_details=True, raw=False,
            c2_delay_df=self.eagerness, norm_delay_m=None,
            norm_delay_sd=None
        )

        if len(parsed_results) == 0:
            return None

        for result in parsed_results.values():
            if len(result['features']) > 0:
                features = [models.RealEstateFeature(
                    name=feature) for feature in result['features']]

                result['features'] = features

            models.RealEstate(**result).save()

        worker_job.update(fetched=True)

        print(f'Finished working on job {worker_job}.')


    def _run_loop(self):
        while self._running:
            worker_jobs = list(models.ZapFetchJob.objects.filter(page=0))
            shuffle(worker_jobs)

            processes = min(self.processes, len(worker_jobs))

            if processes == 0:
                logger.error('No fetch jobs to detail.')
                time.sleep(3)

            else:
                print(f'Spawning {self.processes} Worker processes.')
                p = Pool(processes)
                p.map_async(self.work, worker_jobs)


    def run(self):
        self._running = True
        thread = Thread(target=self._run_loop)
        thread.start()

    def stop(self):
        self._running = False


class Pipeline(object):

    def __init__(self, states=None, eagerness=MEDIUM_EAGERNESS, processes=5):
        self.states = states
        self.eagerness = eagerness
        self.processes = processes

    def run(self):
        self.general = General(states=self.states, processes=self.processes,
                               eagerness=self.eagerness)

        pool = self.general.run()
        pool.get()

        print('Finished listing locations. Starting scouting places')

        self.scout = Scout(processes=self.processes, eagerness=self.eagerness)
        pool = self.scout.run()
        pool.get()

        # self.worker = Worker(processes=self.processes,
        #                      eagerness=self.eagerness)

        # self.worker.run()

    def stop(self):
        self.worker.stop()
