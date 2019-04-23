import urllib

from scipy import stats

from ..utils.common import parse_delay_args
from ..utils.request import fetch_json, GET, POST


URL_ASYNC_SEARCH = 'https://www.zapimoveis.com.br/Busca/RetornarBusca' \
                   'Assincrona'

URL_STATES_LIST = 'https://www.zapimoveis.com.br/Localidade/ListarEstados'

URL_CITIES_AND_REGIONS_LIST = 'https://www.zapimoveis.com.br/Localidade/' \
                   'ListarCidadesLocalidades'

URL_REGIONS_LIST = 'https://www.zapimoveis.com.br/Localidade/' \
                   'ListarCidadesZonas'

URL_NEIGHBORHOODS_LIST = 'https://www.zapimoveis.com.br/Localidade/' \
                         'ListarBairros'

URL_RS_DETAIL = 'https://www.zapimoveis.com.br/BuscaMapa/ObterDetalhe' \
                'ImoveisMapa/'

URL_MAP_SEARCH_URL = 'https://www.zapimoveis.com.br/BuscaMapa/ObterOfertas' \
                     'BuscaMapa/'

HEADERS_ASYNC_SEARCH = {
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7'
                    'MA4YWxkTrZu0gW',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.zapimoveis.com.br/venda/imoveis/'
               'rj+rio-de-janeiro/',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/'
                  '20100101 Firefox/60.0',
    'X-Requested-With': 'XMLHttpRequest',
}

HEADERS_CITIES_AND_REGIONS_LIST = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,fr;q=0.5,'
                       'it;q=0.4',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.zapimoveis.com.br',
    'Referer': 'https://www.zapimoveis.com.br/venda/imoveis/sp+osasco/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

HEADERS_REGIONS_LIST = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,fr;q=0.5,'
                       'it;q=0.4',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.zapimoveis.com.br',
    'Referer': 'https://www.zapimoveis.com.br/venda/imoveis/sp+osasco/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

HEADERS_NEIGHBORHOODS_LIST = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,fr;q=0.5,'
                       'it;q=0.4',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.zapimoveis.com.br',
    'Referer': 'https://www.zapimoveis.com.br/venda/imoveis/sp+osasco/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

HEADERS_STATES_LIST = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.zapimoveis.com.br',
    'Referer': 'https://www.zapimoveis.com.br/Scripts/modulos/buscaMapa/'
    'workerMapa.js',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'refer': 'https://www.zapimoveis.com.br/?__zt=tnrl:v1',
    'x-requested-with': 'XMLHttpRequest'
}

HEADERS_RS_DETAIL = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.zapimoveis.com.br',
    'Referer': 'https://www.zapimoveis.com.br/busca-mapa',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

HEADERS_MAP_SEARCH = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Origin': 'https://www.zapimoveis.com.br',
    'Referer': 'https://www.zapimoveis.com.br/Scripts/modulos/buscaMapa/'
    'workerMapa.js',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}

REGION_CONVERSION_DICT = {
    'Zona': 'region',
    'Bairro': 'neighborhood',
    'Cidade': 'region',
}

ZAP_FIELDS_TRANSLATION_DICT = {
        'ID': 'asset_id',
        'CodigoOfertaZAP': 'asset_id',
        'DetalhesOferta': 'ad_details',
        'SubTipoOferta': 'ad_subtype',
        'TipoOfertaID': 'ad_type_id',
        'UrlFicha': 'ad_url',
        'Endereco': 'address',
        'CodigoAnunciante': 'advertiser_id',
        'UrlLogotipoCliente': 'advertiser_logo_url',
        'NomeAnunciante': 'advertiser_name',
        'IndLeilao': 'auction_status',
        'UrlOfertaLeilaoVip': 'auction_url',
        'Dormitorios': 'bedrooms',
        'CodImobiliaria': 'broker_code',
        'CodigoOfertaImobiliaria': 'broker_offer_code',
        'DistanciaOnibus': 'bus_station_distance',
        'Cidade': 'city',
        'Observacao': 'commentary',
        'PrecoCondominio': 'condominium_price',
        'EstagioObra': 'construction_stage',
        'Caracteristicas': 'features',
        'AreaUtil': 'floor_area',
        'Vagas': 'garage_spaces',
        'possuiTelefone': 'has_phone',
        'PossuiQualidadeTotal': 'has_total_quality',
        'DataAtualizacaoHumanizada': 'humanized_update_date',
        # 'Fotos': 'images_urls',
        'indOferta': 'ind_oferta',
        'DataUltimoAnuncio': 'last_announcement_date',
        'Latitude': 'lat_coords',
        'Longitude': 'lng_coords',
        'FotoPrincipal': 'main_image_url',
        'DormitoriosMaxima': 'max_bedrooms',
        'VagasMaxima': 'max_garage_spaces',
        'SuitesMaxima': 'max_suites',
        'Bairro': 'neighborhood',
        'TipoDaOferta': 'offer_type',
        'CidadeOficial': 'official_city',
        'BairroOficial': 'official_neighborhood',
        'TituloPagina': 'page_title',
        'IndDistrato': 'payment_problems',
        # 'Telefones': 'phones',
        'PrecoM2': 'price_m2',
        'ValorIPTU': 'property_tax',
        'SubTipoImovel': 'property_type',
        'PrecoLocacao': 'rent_price',
        'NotaLocacao': 'renting_score',
        'PrecoVenda': 'sell_price',
        'NotaVenda': 'selling_score',
        'Estado': 'state',
        'Suites': 'suites',
        'DistanciaMetro': 'subway_station_distance',
        'AreaTotal': 'total_area',
        'ZapID': 'zap_id',
        'CEP': 'zip_code',
    }

def get_states_list(
        raw=False, c2_delay_df=None, norm_delay_m=None, norm_delay_sd=None):
    """Retrieves the Zap Imóveis states list.

    State description example:
        {'SP': 'Sao Paulo'}

    The key (state_symbol) must be used as the state kwarg into other methods.

    If raw is True the raw response will be returned.

    Kwargs:
        raw: boolean
        c2_delay_df: float or None
        norm_delay_m: float or None
        norm_delay_sd: float or None

    Returns:
        {state_symbol: state_name}
    """
    parse_delay_args(**locals())

    result = fetch_json(URL_STATES_LIST, method=POST,
                        headers=HEADERS_STATES_LIST)

    if raw:
        return result

    return {item['id']: item['text'] for item in result}


def get_cities_and_regions_list(
        state=None, with_text=False, raw=False, force_region=False,
        c2_delay_df=None, norm_delay_m=None, norm_delay_sd=None):
    """Retrieves the Zap Imóveis cities and regions list.

    If state is None it will return the result for all states listed by the
    function get_states_list.

    There are 3 types of locations. When with_text if False, these are the
    exemples of possible results:
        - Region:
            {'region': 'SAO PAULO', state: 'SP'}
        - Neighborhood:
            {'neighborhood': 'Aldeia da Serra', state: 'SP'}
        - City:
            {'city': 'Região de Ribeirão Preto', state: 'SP'}

    If with_text is True a more raw version will be returned:
        - Region:
            {'region_type': 'Zona', 'region_type_text': 'SAO PAULO',
             'text': 'Capital', state: 'SP'}
        - Neighborhood:
            {'region_type': 'Bairro', 'region_type_text': 'Aldeia da Serra',
             'text': 'Aldeia da Serra', state: 'SP'}
        - City:
            {'region_type': 'Cidade',
             'region_type_text': 'Região de Ribeirão Preto',
             'text': 'Região de Ribeirão Preto', state: 'SP'}

    The value of the region type (region, neighborhood or city) must be used to
    populate other searches.

    If raw is True the raw response will be returned.

    If force_region is True the key of all regions will be 'region'. Be
    advisesd that if with_text is True this parameter will be ignored.

    kwargs:
        state: str or None
        with_text: bool
        raw: bool
        force_region: bool
        c2_delay_df: float or None
        norm_delay_m: float or None
        norm_delay_sd: float or None

    Returns:
        [location]
            if with_text is False:
                location: {'region': str, 'state': str} or
                          {'neighborhood': str, 'state': str} or
                          {'city': str, 'state': str}
            if with_text is True:
                location: {'region_type': str, 'region_type_text': str,
                           'text': str, 'state': str}
    """
    parse_delay_args(**locals())

    # If the user don't provide the state  we should search for them
    if state is None:
        concat_result = []
        for state in get_states_list().keys():
            concat_result += get_cities_and_regions_list(
                state=state, with_text=with_text, raw=raw)

        return concat_result

    result = fetch_json(
        URL_CITIES_AND_REGIONS_LIST, method=POST, data=f'estado={state}',
        headers=HEADERS_CITIES_AND_REGIONS_LIST)

    if raw:
        return result

    # We will remove the 'Tipo' key in order to determine the key of the result
    # list
    result.pop('Tipo', None)

    result_list_key = list(result.keys())[0]

    if with_text:
        return [{
                'region_type': item['id'].split('|')[0],
                'region_type_text': item['id'].split('|')[1],
                'text': item['text'],
                'state': state,
            } for item in result[result_list_key]]

    else:
        if force_region:
            return [{
                'region': item['id'].split('|')[1],
                'state': state,
            } for item in result[result_list_key]]
        else:
            return [{
                REGION_CONVERSION_DICT[item['id'].split('|')[0]]:
                    item['id'].split('|')[1],
                'state': state,
            } for item in result[result_list_key]]


def get_neighborhoods_list(
        state=None, region=None, raw=False, lite=True, c2_delay_df=None,
        norm_delay_m=None, norm_delay_sd=None):
    """Retrieves the Zap Imóveis list of neighborhoots within a given region.

    If raw is True the raw response will be returned.

    If lite is True only the state and neighborhood info will be retuned.

    kwargs:
        state: str or None
        region: str or None
        raw: bool
        lite: bool
        c2_delay_df: float or None
        norm_delay_m: float or None
        norm_delay_sd: float or None

    Returns:
        [neighborhood]
            if lite is True:
                neighborhood: {'neighborhood: str, 'state': str}
            if lite is True:
                neighborhood: {'code': int, 'name': str, 'state': str,
                               'region': str}
    """
    parse_delay_args(**locals())

    # If the user don't provide either the state or the region we should search
    # for them
    if state is None or region is None:
        regions = get_cities_and_regions_list(
            state=state, with_text=False, raw=False, force_region=False,
            c2_delay_df=None, norm_delay_m=None, norm_delay_sd=None)

        partial_results = []
        to_process_regions = []

        for region in regions:
            if 'neighborhood' in region.keys():
                partial_results += [region]
            else:
                to_process_regions += [region]

        for region in to_process_regions:
            partial_results += get_neighborhoods_list(
                **region, raw=raw, lite=lite, c2_delay_df=c2_delay_df,
                norm_delay_m=norm_delay_m, norm_delay_sd=norm_delay_sd)

        return partial_results

    region = urllib.parse.quote(region)

    result = fetch_json(
        URL_NEIGHBORHOODS_LIST, method=POST,
        data=f'estado={state}&localidade={region}&cidade=&zona=',
        headers=HEADERS_NEIGHBORHOODS_LIST)

    if raw:
        return result

    region = urllib.parse.unquote(region)

    parsed_result = []
    result = result['Data']

    if lite:
        for letter_item in result:
            parsed_result += [{
                'neighborhood': item['Nome'],
                'state': state,
            } for item in letter_item['Bairros']]
    else:
        for letter_item in result:
            parsed_result += [{
                    'code': item['Codigo'],
                    'name': item['Nome'],
                    'state': state,
                    'region': region,
            } for item in letter_item['Bairros']]

    return parsed_result


def get_real_state_details(item_id, parse=True):
    """TODO add documentation

    """
    parse_delay_args(**locals())
    result = fetch_json(
        URL_RS_DETAIL, method=POST, data=f'listIdImovel=%5B{item_id}%5D',
        headers=HEADERS_RS_DETAIL)

    if not parse:
        return result

    result = result['Resultado']
    if len(result) == 0:
        return {}

    result = result[0]

    return {
        ZAP_FIELDS_TRANSLATION_DICT[key]: value
        for key, value in result.items()
        if ZAP_FIELDS_TRANSLATION_DICT.get(key, False)
    }


def get_search_results(
        max_price=2147483647, neighborhood='Area Octogonal', city_side='',
        city='', state='DF', page=None, get_details=True, raw=False,
        c2_delay_df=None, norm_delay_m=None, norm_delay_sd=None):
    """Retrieves the Zap Imóveis search results.

    This function uses the Zap Imóveis search engine to retrieve real estate
    data.

    So far this function works using only the neighborhood and the state data.

    Use it with caution since it retrieces a lot of data from the webserver.

    kwargs:
        max_price: int
        neighborhood: str
        city_side: str
        city: str
        state: str
        page: int
        c2_delay_df: float or None
        norm_delay_m: float or None
        norm_delay_sd: float or None


    Returns:
        (number_of_pages, current_page, {asset_id: asset})
            asset: {
                'advertiser_id': int,
                'construction_stage': int,
                'ad_url': str,
                'humanized_update_date': str,
                'asset_id': int,
                'broker_offer_code': str,
                'neighborhood': str,
                'official_neighborhood': str,
                'address': str,
                'city': str,
                'official_city': str,
                'state': str,
                'subway_station_distance': str,
                'bus_station_distance': str,
                'phones': [str],
                'has_total_quality': bool,
                'advertiser_logo_url': str,
                'advertiser_name': str,
                'ad_subtype': str,
                'broker_code': int,
                'has_phone': bool,
                'offer_type': str,
                'zap_id': str,
                'payment_problems': bool,
                'auction_status': bool,
                'auction_url': str,
                'ad_details': str,
                'condominium_price': str,
                'property_tax': str,
                'commentary': str,
                'zip_code': str,
                'page_title': str,
                'property_type': str or None,
                'features': [str],
                'lat_coords': str,
                'lng_coords': str,
            }
    """
    parse_delay_args(**locals())

    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n' \
              'Content-Disposition: form-data; ' \
              'name=\"formato\"\r\n\r\nlista\r\n' \
              '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n' \
              'Content-Disposition: form-data; ' \
              'name=\"hashFragment\"\r\n\r\n{\"' \
              f'precomaximo\":\"{max_price}\",' \
              '\"parametrosautosuggest\":[{' \
              f'\"Bairro\":\"{neighborhood}\",\"' \
              f'Zona\":\"{city_side}\",\"Cidade\":\"{city}\",' \
              f'\"Agrupamento\":\"\",\"Estado\":\"{state}\"' \
              '}],' \
              f'\"pagina\":{page},\"ordem\":\"DataAtualizacao\",' \
              '\"paginaOrigem\":\"ResultadoBusca\",\"semente\":' \
              '\"1581296682\",\"formato\":\"Lista\"}\r\n------WebKitFormB' \
              'oundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; ' \
              'name=\"ordenacaoSelecionada\"\r\n\r\nDataAtualizacao\r\n--' \
              '----WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Dispositi' \
              f'on: form-data; name=\"paginaAtual\"\r\n\r\n{page}\r\n------WebK' \
              'itFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form' \
              '-data; name=\"pathName\"\r\n\r\n/venda/imoveis/rj+rio-de-j' \
              'aneiro/\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nCont' \
              'ent-Disposition: form-data; name=\"tipoOferta\"\r\n\r\nImo' \
              'vel\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'

    # User wants us to fetch all pages
    if page is None and not raw:
        # First we neet to find out the ammout of pages
        number_of_pages, current_page, results = get_search_results(
            max_price=max_price, neighborhood=neighborhood,
            city_side=city_side, city=city, state=state, page=1,
            get_details=get_details, raw=raw, c2_delay_df=c2_delay_df,
            norm_delay_m=norm_delay_m, norm_delay_sd=norm_delay_sd)

        for page in range(2, number_of_pages + 1):
            _, _, p_results = get_search_results(
                max_price=max_price, neighborhood=neighborhood,
                city_side=city_side, city=city, state=state, page=page,
                get_details=get_details, raw=raw, c2_delay_df=c2_delay_df,
                norm_delay_m=norm_delay_m, norm_delay_sd=norm_delay_sd)

            results = {
                **results,
                **p_results,
            }

        return results


    results = fetch_json(URL_ASYNC_SEARCH, method=POST, data=payload,
                        headers=HEADERS_ASYNC_SEARCH)

    if raw:
        return results

    results = results['Resultado']
    number_of_pages = results['QuantidadePaginas']
    current_page = results['PaginaAtual']
    results = results['Resultado']

    parsed_results = {}

    for result in results:
        parsed_results[result['CodigoOfertaZAP']] = {
            ZAP_FIELDS_TRANSLATION_DICT[key]: value
            for key, value in result.items()
            if ZAP_FIELDS_TRANSLATION_DICT.get(key, False)
        }

        parsed_results[result['CodigoOfertaZAP']]['web_source'] = 'z'

    if get_details:
        for asset_id, details in parsed_results.items():
            parsed_results[asset_id] = {
                **details,
                **get_real_state_details(asset_id)
            }

    return number_of_pages, current_page, parsed_results


# Currently not in use
def get_real_state_list(
        lat='-23.533252602847163', lon='-46.72576324007906',
        lat_min='-23.536708781721547', lon_min='-46.73071996233858',
        lat_max='-23.529796333175693', lon_max='-46.72080651781954'):
    parse_delay_args(**locals())
    return fetch_json(
        URL_MAP_SEARCH_URL, method=POST, headers=HEADERS_MAP_SEARCH, data={
            "parametrosBusca": '{"CoordenadasAtuais": {'
                f'"Latitude":{lat},"Longitude":{lon}'
                '}, "CoordenadasMinimas": {'
                f'"Latitude":{lat_min},"Longitude":{lon_min}'
                '},'
                ' "CoordenadasMaximas": {'
                f'"Latitude":{lat_max},"Longitude":{lon_max}'
                '}, "PrecoMinimo":"0","AreaUtilMinima":"0","Tr'
                'ansacao":"Venda","TipoOferta":"Imovel"}'
        })


# Currently not in use.
def get_city_regions_list(
        state='SP', location='SAO PAULO', raw=False, with_text=False,
        c2_delay_df=None, norm_delay_m=None, norm_delay_sd=None):
    """Retrieves the Zap Imóveis list of regions of a given city.

    There are 3 types of locations. When with_text if False, these are the
    exemples of possible results:
        - Region:
            {'region': 'SAO PAULO', state: 'SP'}
        - Neighborhood:
            {'neighborhood': 'Aldeia da Serra', state: 'SP'}
        - City:
            {'city': 'Região de Ribeirão Preto', state: 'SP'}

    If with_text is True a more raw version will be returned:
        - Region:
            {'region_type': 'Zona', 'region_type_text': 'SAO PAULO',
             'text': 'Capital', state: 'SP'}
        - Neighborhood:
            {'region_type': 'Bairro', 'region_type_text': 'Aldeia da Serra',
             'text': 'Aldeia da Serra', state: 'SP'}
        - City:
            {'region_type': 'Cidade',
             'region_type_text': 'Região de Ribeirão Preto',
             'text': 'Região de Ribeirão Preto', state: 'SP'}

    The value of the region type (region, neighborhood or city) must be used to
    populate other searches.

    If raw is True the raw response will be returned.

    kwargs:
        state: str
        location: str
        with_text: bool
        raw: bool
        c2_delay_df: int or None
        norm_delay_m: int or None
        norm_delay_sd: int or None

    Returns:
        [location]
            if with_text is False:
                location: {'region': str, 'state': str} or
                          {'neighborhood': str, 'state': str} or
                          {'city': str, 'state': str}
            if with_text is True:
                location: {'region_type': str, 'region_type_text': str,
                           'text': str, 'state': str}
    """
    parse_delay_args(**locals())

    location = urllib.parse.quote(location)  # Maybe this isn't necessary

    result = fetch_json(
        URL_REGIONS_LIST, method=POST,
        data=f'estado={state}&localidade={location}&tipo=Zona',
        headers=HEADERS_REGIONS_LIST)

    # We will remove the 'Tipo' key in order to determine the key of the result
    # list
    result.pop('Tipo', None)

    result_list_key = list(result.keys())[0]

    if raw:
        return result

    if with_text:
        return [{
                'region_type': item['id'].split('|')[0],
                'region_type_text': item['id'].split('|')[1],
                'text': item['text'],
                'state': state,
                } for item in result[result_list_key]]

    else:
        return [{
            REGION_CONVERSION_DICT[item['id'].split('|')[0]]:
                item['id'].split('|')[1],
            'state': state,
        } for item in result[result_list_key]]
