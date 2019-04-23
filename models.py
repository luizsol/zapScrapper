# -*- coding: utf-8 -*-
import datetime
import json

import numpy as np
import mongoengine


mongoengine.connect(db='zap_dados', host='localhost', port=27017)


class RealEstateFeature(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(required=False)


class RealEstate(mongoengine.Document):
    """Represents a real state ad via the Mongoengine ORM.
    TODO this documentation
    """
    WEB_SOURCE = (
        ('z', 'Zap Imóveis'),
        ('v', 'Viva Real'),
    )

    # ID, CodigoOfertaZAP
    asset_id = mongoengine.IntField(required=True)
    # DetalhesOferta
    ad_details = mongoengine.StringField(required=False)
    # SubTipoOferta
    ad_subtype = mongoengine.IntField(min_value=0, required=False)
    # TipoOfertaID
    ad_type_id = mongoengine.IntField(required=False)
    # UrlFicha
    ad_url = mongoengine.StringField(required=False)
    # Endereco
    address = mongoengine.StringField(required=False)
    # CodigoAnunciante
    advertiser_id = mongoengine.IntField(required=False)
    # UrlLogotipoCliente
    advertiser_logo_url = mongoengine.StringField(required=False)
    # NomeAnunciante
    advertiser_name = mongoengine.StringField(required=False)
    # IndLeilao
    auction_status = mongoengine.BooleanField(required=False)
    # UrlOfertaLeilaoVip
    auction_url = mongoengine.StringField(required=False)
    # Dormitorios
    bedrooms = mongoengine.IntField(min_value=0, required=False)
    # CodImobiliaria
    broker_code = mongoengine.IntField(min_value=0, required=False)
    # CodigoOfertaImobiliaria
    broker_offer_code = mongoengine.StringField(required=False)
    # DistanciaOnibus
    bus_station_distance = mongoengine.StringField(required=False)
    # Cidade
    city = mongoengine.StringField(required=False)
    # Observacao
    commentary = mongoengine.StringField(required=False)
    # PrecoCondominio
    condominium_price = mongoengine.StringField(required=False)
    # EstagioObra
    construction_stage = mongoengine.IntField(required=False)
    created_at = mongoengine.DateTimeField()
    # Caracteristicas
    features = mongoengine.EmbeddedDocumentListField(RealEstateFeature)
    # AreaUtil
    floor_area = mongoengine.FloatField(required=False)
    # Vagas
    garage_spaces = mongoengine.IntField(min_value=0, required=False)
    # possuiTelefone
    has_phone = mongoengine.BooleanField(required=False)
    # PossuiQualidadeTotal
    has_total_quality = mongoengine.BooleanField(required=False)
    # DataAtualizacaoHumanizada
    humanized_update_date = mongoengine.StringField(required=False)
    # Fotos
    # images_urls = mongoengine.EmbeddedDocumentListField(
    #   mongoengine.StringField)
    # indOferta
    ind_oferta = mongoengine.BooleanField(required=False)
    # DataUltimoAnuncio
    last_announcement_date = mongoengine.DateTimeField(required=False)
    # Coordenadas['Latitude']
    lat_coords = mongoengine.DecimalField(precision=7, required=False)
    # Coordenadas['Longitude']
    lng_coords = mongoengine.DecimalField(precision=7, required=False)
    # FotoPrincipal
    main_image_url = mongoengine.StringField(required=False)
    # DormitoriosMaxima
    max_bedrooms = mongoengine.IntField(min_value=0, required=False)
    # VagasMaxima
    max_garage_spaces = mongoengine.IntField(min_value=0, required=False)
    # SuitesMaxima
    max_suites = mongoengine.IntField(min_value=0, required=False)
    # Bairro
    neighborhood = mongoengine.StringField(required=False)
    # TipoDaOferta
    offer_type = mongoengine.StringField(required=False)
    # CidadeOficial
    official_city = mongoengine.StringField(required=False)
    # BairroOficial
    official_neighborhood = mongoengine.StringField(required=False)
    # TituloPagina
    page_title = mongoengine.StringField(required=False)
    # IndDistrato
    payment_problems = mongoengine.BooleanField(required=False)
    # Telefones
    # phones = mongoengine.EmbeddedDocumentListField(mongoengine.StringField)
    # PrecoM2
    price_m2 = mongoengine.FloatField(required=False)
    # ValorIPTU
    property_tax = mongoengine.StringField(required=False)
    # SubTipoImovel
    property_type = mongoengine.StringField(required=False)
    # PrecoLocacao
    rent_price = mongoengine.DecimalField(precision=2, required=False)
    # NotaLocacao
    renting_score = mongoengine.DecimalField(precision=10, required=False)
    # PrecoVenda
    sell_price = mongoengine.DecimalField(precision=2, required=False)
    # NotaVenda
    selling_score = mongoengine.DecimalField(precision=10, required=False)
    # Estado
    state = mongoengine.StringField(required=False)
    # Suites
    suites = mongoengine.IntField(min_value=0, required=False)
    # DistanciaMetro
    subway_station_distance = mongoengine.StringField(required=False)
    # AreaTotal
    total_area = mongoengine.FloatField(required=False)
    web_source = mongoengine.StringField(max_length=1, choices=WEB_SOURCE,
                                         required=True)
    # ZapID
    zap_id = mongoengine.StringField(required=False)
    # CEP
    zip_code = mongoengine.StringField(required=False)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(RealEstate, self).save(*args, **kwargs)

    def __str__(self):
        return f'ID: {self.asset_id}, Sell Price: {self.sell_price}, ' \
               f'Rent Price: {self.rent_price}'

    def __repr__(self):
        return f'RealEstate({self}'


class ZapFetchJob(mongoengine.Document):
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    fetched = mongoengine.BooleanField(required=True, default=False)
    in_progress = mongoengine.BooleanField(required=True, default=False)
    neighborhood = mongoengine.StringField(required=False)
    page = mongoengine.IntField(min_value=0, required=True, default=0)
    state = mongoengine.StringField(required=False)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(ZapFetchJob, self).save(*args, **kwargs)
