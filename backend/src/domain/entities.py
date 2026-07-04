# backend/src/domain/entities.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from decimal import Decimal
import pandas as pd

from ..helpers.common.formatting.number_formatting_processing import NumberFormattingProcessing

class CommonBusinessRules(BaseModel):
    @staticmethod
    def brazilian_formatted_value(value: Optional[float | int]) -> Optional[str]:
        if value is None:
            return "—"
        truncated_value = NumberFormattingProcessing.to_decimal_truncated(value, value_to_ignore=None, precision=2)
        
        if isinstance(value, (float)):
            return NumberFormattingProcessing.format_number_brazilian(float(truncated_value))
        elif isinstance(value, (int)):
            return NumberFormattingProcessing.format_number_brazilian(int(truncated_value))
        
        return "—"
    
    @staticmethod
    def brazilian_formatted_value_ignore_two_zeros(value: Optional[float | int]) -> Optional[str]:
        if value is None:
            return "—"
        truncated_value = NumberFormattingProcessing.to_decimal_truncated(value, value_to_ignore=None, precision=2)
        
        if isinstance(value, (float)):
            return NumberFormattingProcessing.format_number_brazilian_ignore_two_zeros(float(truncated_value))
        elif isinstance(value, (int)):
            return NumberFormattingProcessing.format_number_brazilian_ignore_two_zeros(int(truncated_value))
        
        return "—"
    
    @staticmethod
    def brazilian_formatted_value_integer(value: Optional[float | int]) -> Optional[str]:
        if value is None:
            return "—"
        truncated_value = NumberFormattingProcessing.to_decimal_truncated(value, value_to_ignore=None, precision=2)
        
        if isinstance(value, (float, int)):
            return NumberFormattingProcessing.format_number_brazilian_ignore_two_zeros(int(truncated_value))

        return "—"

    @staticmethod
    def brazilian_formatted_value_currency_short(value: Optional[float | int]) -> Optional[str]:
        """
        Format a monetary value in short scale (Mi/Bi) with Brazilian conventions.

        >= 1.000.000.000: divides by 1 Bi, truncates to 2 decimal places -> 'R$ 2,00 Bi'
        >= 1.000.000:     divides by 1 Mi, truncates to 2 decimal places -> 'R$ 2,00 Mi'
        Smaller values fall back to the plain Brazilian currency format.
        """
        if value is None:
            return "—"

        abs_value = abs(value)
        if abs_value >= 1_000_000_000:
            scaled = Decimal(str(value)) / Decimal(1_000_000_000)
            suffix = "Bi"
        elif abs_value >= 1_000_000:
            scaled = Decimal(str(value)) / Decimal(1_000_000)
            suffix = "Mi"
        else:
            return f"R$ {CommonBusinessRules.brazilian_formatted_value(value)}"

        truncated_value = NumberFormattingProcessing.to_decimal_truncated(scaled, value_to_ignore=None, precision=2)
        formatted_value = NumberFormattingProcessing.format_number_brazilian(float(truncated_value))
        return f"R$ {formatted_value} {suffix}"



class County(BaseModel):
    county_id: int
    county: str
    state: str
    region: str
    display: Optional[str] = None
    
class RiskFactor(BaseModel):
    risk_id: Optional[int] = None
    detail_id: Optional[int] = None
    sep_id: Optional[int] = None
    county_id: Optional[int] = None
    legend_id: Optional[int] = None
    
    sep: Optional[str] = None
    risk: Optional[str] = None
    detail: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    
    level: Optional[int] = None
    year: Optional[str] = None
    value: Optional[float] = None
    color: Optional[str] = None
    current_value: Optional[float] = None
    current_value_color: Optional[str] = None
    future_value: Optional[float] = None
    future_color: Optional[str] = None
    imageurl: Optional[str] = None
    risk_url: Optional[str] = None

class RiskFactorReport(BaseModel):
    risk_factors: List[RiskFactor]
        
    @property
    def formatted_data_dict(self) -> List[Dict[str, Any]]:
        grouped_risks = {}
        
        for rf in self.risk_factors:
            if rf.risk_id not in grouped_risks:
                grouped_risks[rf.risk_id] = {
                    "county_id": rf.county_id,
                    "risk_id": rf.risk_id,
                    "sep": rf.sep,
                    "risk": rf.risk,
                    "county": rf.county,
                    "state": rf.state,
                    "color": rf.color,
                    "imageurl": rf.imageurl,
                    "risk_url": rf.risk_url,
                    "current_value": rf.current_value,
                    "current_value_color": rf.current_value_color,
                    "formatted_current_value": CommonBusinessRules.brazilian_formatted_value(rf.current_value),
                    
                    "future_value": rf.future_value,
                    "future_color": rf.future_color,
                    "formatted_future_value": CommonBusinessRules.brazilian_formatted_value(rf.future_value),
                    
                    "Ameaça": "",
                    "Exposição": "",
                    "Vulnerabilidade": "",
                    "Sensibilidade": "",
                    "Capacidade adaptativa": ""
                }
            
            if rf.detail:
                # If the detail is "capacidade adaptativa", we want to keep it as is, otherwise we can capitalize it
                # coluna_transposta = rf.detail.capitalize() if rf.detail.lower() == "capacidade adaptativa" else rf.detail
                
                grouped_risks[rf.risk_id][rf.detail] = rf.value
                grouped_risks[rf.risk_id][f"{rf.detail}_color"] = rf.color
                
        # Apply formatting to the specific columns after all values have been assigned
        for key, item in grouped_risks.items():
            for col in ["Ameaça", "Exposição", "Vulnerabilidade", "Sensibilidade", "Capacidade adaptativa"]:
                if col in item and item[col] is not None:
                    item[col] = CommonBusinessRules.brazilian_formatted_value(item[col])
                
        return list(grouped_risks.values())

    @property
    def formatted_data_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.formatted_data_dict)

class MunicipalIndicators(BaseModel):
    
    # Territorial fields
    county_id: Optional[int] = None
    area: Optional[float] = None
    regic_influencia: Optional[str] = None
    pop_urb_pessoas: Optional[float] = None # TODO: apply brazilian formatting to this field in the report
    pop_urb_pct: Optional[float] = None
    pop_rural_pessoas: Optional[float] = None
    pop_rural_pct: Optional[float] = None
    densidade_urb: Optional[float] = None
    pib: Optional[float] = None
    
    # Population characteristics fields
    mulheres: Optional[float] = None
    pretos_pardos: Optional[float] = None
    pop_inf: Optional[float] = None
    pop_idosa: Optional[float] = None
    indigenas: Optional[float] = None
    quilombolas: Optional[float] = None
    
    # Socioeconomic conditions
    ## IDH and related indicators
    idh_m: Optional[float] = None
    renda_media: Optional[float] = None
    escolaridade: Optional[float] = None
    expec_vida: Optional[float] = None
    
    ## Social programs
    firjan: Optional[float] = None
    bolsa_familia: Optional[float] = None
    alfabet: Optional[float] = None
    
    ## Infrastructure and services
    leito_hab: Optional[float] = None
    prof_hab: Optional[float] = None
    cob_vacinal: Optional[float] = None
    
    ## Vulnerable populations
    pop_fav: Optional[float] = None
    dom_semi_inadeq: Optional[float] = None
    
    ## Access to services
    acesso_agua2: Optional[float] = None
    acesso_esgoto: Optional[float] = None
    acesso_energia: Optional[float] = None
    acesso_lixo: Optional[float] = None
    
    # MOBILIDADE POPULATION
    imig_regist: Optional[float] = None
    solic_refugio: Optional[float] = None
    imigrantes: Optional[float] = None
    tx_turismo: Optional[float] = None
    

class MunicipalIndicatorsReport(BaseModel):
    municipal_indicators: MunicipalIndicators
    
    @property
    def formatted_data_dict(self) -> Dict[str, Any]:
        data = self.municipal_indicators.dict()
        for key, value in data.items():
            if value is None:
                data[key] = "—"
                continue
            if key == "area":
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} km²"
            elif key in ["renda_media", "pib"]:
                data[key] = f"R$ {CommonBusinessRules.brazilian_formatted_value(value)}"
            elif key == "densidade_urb":
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value_integer(value)} hab/km²"
            elif key in ["pop_urb_pct", "pop_rural_pct", "mulheres", "pretos_pardos", "pop_inf", "pop_idosa", "imigrantes", "indigenas", "quilombolas", "alfabet", "cob_vacinal"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)}%"
            elif key in ["bolsa_familia"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)}% das famílias pobres" 
            elif key in ["firjan", "acesso_agua2", "acesso_esgoto", "acesso_energia", "acesso_lixo"]:
                data[key] = CommonBusinessRules.brazilian_formatted_value(value)
            elif key in ["pop_urb_pessoas", "pop_rural_pessoas"]:
                if not isinstance(value, (float, int)):
                    data[key] = "—"
                else:
                    data[key] = CommonBusinessRules.brazilian_formatted_value_ignore_two_zeros(value)
            elif key in ["leito_hab", "prof_hab"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} para cada 1.000 hab"
            elif key in ["escolaridade", "expec_vida"]:                
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value_ignore_two_zeros(value)} anos"
            elif key in ["pop_fav", "dom_semi_inadeq"]:
                data[key] = CommonBusinessRules.brazilian_formatted_value_ignore_two_zeros(value)
            elif key == "idh_m":
                if not isinstance(value, (float, int)):
                    data[key] = "—"
                elif value >= 0.800:
                    data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} (Muito Alto)"
                elif 0.700 <= value < 0.800:
                    data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} (Alto)"
                elif 0.550 <= value < 0.700:
                    data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} (Médio)"
                else:
                    data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} (Baixo)"
            
            elif key in ["imig_regist"]:
                data[key] = CommonBusinessRules.brazilian_formatted_value(value)
            elif key in ["solic_refugio", "imigrantes", "tx_turismo"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)}%"
            
            
        return data

    @property
    def formatted_data_df(self) -> pd.DataFrame:
        return pd.DataFrame([self.formatted_data_dict])

"""
Tabela ClimateProjection

Dados de exeplo da tabela: 
geocode|nm_munic            |temp_med|temp_med_tend|temp_max|temp_max_tend|temp_min|temp_min_tend|temp_med_otim|temp_max_otim|temp_min_otim|temp_med_pes|temp_max_pes|temp_min_pes|dias_secos|dias_secos_tend|dias_chuva|dias_chuva_tend|chuva_ext|chuva_ext_tend|precip|precip_tend|dias_secos_otim|dias_chuva_otim|chuva_ext_otim|precip_otim|dias_secos_pes|dias_chuva_pes|chuva_ext_pes|precip_pes|nivel_mar|nivel_mar_tend|nivel_mar_30|nivel_mar_50|county_id|
-------+--------------------+--------+-------------+--------+-------------+--------+-------------+-------------+-------------+-------------+------------+------------+------------+----------+---------------+----------+---------------+---------+--------------+------+-----------+---------------+---------------+--------------+-----------+--------------+--------------+-------------+----------+---------+--------------+------------+------------+---------+
1300607|Benjamin Constant/AM|   25.96|         0.18|   29.28|         0.24|   22.63|         0.12|         1.29|         2.18|         0.66|        1.64|        2.85|        0.98|     55.19|           6.25|      4.61|          -0.43|    51.64|         -8.27|  4.96|      -0.23|           1.51|          -3.79|          3.48|       0.29|          2.23|         -6.11|         3.91|      0.33|         |              |            |            |     5468|
2505600|Diamante/PB         |   26.91|          0.1|    32.2|         0.13|   21.61|         0.07|         1.01|         1.51|         0.39|        1.25|        1.81|        0.54|     12.33|           0.28|      7.06|           0.06|   161.25|         15.67| 14.16|       1.35|          11.21|          -1.31|          3.63|       1.12|         16.48|          -1.0|         3.67|      1.17|         |              |            |            |     4054|
3152204|Porteirinha/MG      |   24.23|         0.27|   29.17|         0.36|   19.28|         0.19|         1.13|          2.0|         0.45|        1.39|        2.36|        0.67|     23.19|          -0.08|      6.26|           0.33|   178.78|          6.23| 13.37|       0.08|            0.0|            0.0|           0.0|        0.0|           0.0|           0.0|          0.0|       0.0|         |              |            |            |     1363|
3170800|Várzea da Palma/MG  |    24.1|          0.3|   28.97|         0.42|   19.23|          0.2|         1.21|         1.93|         0.59|        1.51|        2.43|        0.95|     25.55|          -0.08|      6.14|           0.08|   136.16|          11.4| 11.63|       0.44|            0.0|            0.0|           0.0|        0.0|           0.0|           0.0|          0.0|       0.0|         |              |            |            |     1588|
2708204|São Brás/AL         |   26.22|         0.12|   30.01|         0.12|   22.43|         0.11|         0.82|         1.44|         0.48|        1.03|        1.65|        0.68|     14.61|          -0.91|      6.99|          -0.22|    183.3|         14.69| 14.99|      -0.01|            0.0|            0.0|           0.0|        0.0|           0.0|           0.0|          0.0|       0.0|         |              |            |            |     4474|
2600708|Aliança/PE          |   25.73|         0.12|    29.0|         0.12|   22.46|         0.12|         0.88|          1.2|         0.37|        1.08|        1.46|        0.53|     12.81|            0.0|      6.93|          -0.11|   161.87|         21.19| 14.03|       1.49|           3.07|          -1.19|         -1.79|      -0.08|          4.62|         -2.33|        -3.54|      0.03|         |              |            |            |     4209|
3138401|Leopoldina/MG       |   22.74|         0.18|   27.05|         0.31|   18.43|         0.08|         0.96|         2.08|         0.22|        1.21|        2.62|        0.71|     47.52|           2.78|      9.92|          -1.02|    139.8|         -6.79| 12.36|        0.5|            0.0|            0.0|           0.0|        0.0|           0.0|           0.0|          0.0|       0.0|         |              |            |            |     1192|
4106605|Cruzeiro do Oeste/PR|   22.84|         0.23|   27.13|         0.32|   18.55|         0.15|          1.2|         2.55|         0.65|        1.55|        3.11|        1.06|     63.59|           0.39|     10.98|          -1.64|   102.51|         -7.71|  9.25|      -0.55|            0.0|            0.0|           0.0|        0.0|           0.0|           0.0|          0.0|       0.0|         |              |            |            |     5112|
4127882|Tunas do Paraná/PR  |   18.48|         0.16|   22.48|         0.19|   14.47|          0.1|          0.9|          1.8|         0.44|        1.16|        2.33|        0.77|     87.29|           10.9|     13.15|          -0.68|   117.61|          3.73| 10.66|        0.0|            0.0|            0.0|           0.0|        0.0|           0.0|           0.0|          0.0|       0.0|         |              |            |            |     5429|
2606200|Goiana/PE           |    25.9|         0.13|   28.51|         0.12|   23.29|         0.14|         0.87|         1.16|          0.4|        1.06|        1.42|        0.55|      12.4|           0.07|      6.74|           0.05|   158.07|         23.45| 13.98|       1.55|            0.0|            0.0|           0.0|        0.0|           0.0|           0.0|          0.0|       0.0|         |              |            |        0.23|     4270|

"""
class ClimateProjection(BaseModel):
    geocode: Optional[int] = None
    nm_munic: Optional[str] = None
    county_id: Optional[int] = None
    
    temp_med: Optional[float] = None
    temp_med_tend: Optional[float] = None
    temp_med_otim: Optional[float] = None
    temp_med_pes: Optional[float] = None


    temp_max: Optional[float] = None
    temp_max_tend: Optional[float] = None
    temp_max_otim: Optional[float] = None
    temp_max_pes: Optional[float] = None

    temp_min_otim: Optional[float] = None
    temp_min: Optional[float] = None
    temp_min_tend: Optional[float] = None
    temp_min_pes: Optional[float] = None
    
    dias_secos: Optional[float] = None
    dias_secos_tend: Optional[float] = None
    dias_secos_otim: Optional[float] = None
    dias_secos_pes: Optional[float] = None


    dias_chuva: Optional[float] = None
    dias_chuva_tend: Optional[float] = None
    dias_chuva_otim: Optional[float] = None
    dias_chuva_pes: Optional[float] = None

    
    chuva_ext_pes: Optional[float] = None
    chuva_ext: Optional[float] = None
    chuva_ext_tend: Optional[float] = None
    chuva_ext_otim: Optional[float] = None

    precip: Optional[float] = None
    precip_tend: Optional[float] = None
    precip_otim: Optional[float] = None
    precip_pes: Optional[float] = None
    
    nivel_mar: Optional[float] = None
    nivel_mar_tend: Optional[float] = None
    nivel_mar_30: Optional[float] = None
    nivel_mar_50: Optional[float] = None
    
class ClimateProjectionReport(BaseModel):
    climate_projection: ClimateProjection
    
    @property
    def formatted_data_dict(self) -> Dict[str, Any]:
        data = self.climate_projection.dict()
        for key, value in data.items():
            if value is None:
                data[key] = "—"
                continue
            
            if key in ["temp_med", "temp_med_tend", "temp_med_otim", "temp_med_pes",
                       "temp_max", "temp_max_tend", "temp_max_otim", "temp_max_pes",
                       "temp_min", "temp_min_tend", "temp_min_otim", "temp_min_pes"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} °C"
            elif key in ["dias_secos", "dias_secos_tend", "dias_secos_otim", "dias_secos_pes",
                         "dias_chuva", "dias_chuva_tend", "dias_chuva_otim", "dias_chuva_pes"]:
                data[key] = CommonBusinessRules.brazilian_formatted_value_integer(value)
            elif key in ["chuva_ext", "chuva_ext_tend", "chuva_ext_otim", "chuva_ext_pes",
                         "precip", "precip_tend", "precip_otim", "precip_pes"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} mm"
            elif key in ["nivel_mar", "nivel_mar_tend", "nivel_mar_30", "nivel_mar_50"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)} mm"
                
        return data

    @property
    def formatted_data_df(self) -> pd.DataFrame:
        return pd.DataFrame([self.formatted_data_dict])


class MunicipalResilienceProfile(BaseModel):
    # Identificação do município
    county_id: Optional[int] = None
    geocode: Optional[int] = None
    
    # Uso do solo
    bioma: Optional[str] = None
    veg_natural: Optional[float] = None
    agropec: Optional[float] = None
    ucs: Optional[str] = None
    ti: Optional[str] = None
    # TODO: Missing fields for : Uso e cobertura da terra
    
    # gestão municipal
    plano_saneam: Optional[str] = None
    plano_residuos: Optional[str] = None
    plano_drenagem: Optional[str] = None
    plano_transporte: Optional[str] = None
    plano_hab: Optional[str] = None
    plano_diretor: Optional[str] = None
    plano_rrd: Optional[str] = None
    plano_conting: Optional[str] = None
    cid_resilientes: Optional[str] = None
    
    # Desastres
    estiagem_incend: Optional[float] = None
    geohidro: Optional[float] = None
    tornad_vendav: Optional[float] = None
    obitos: Optional[float] = None
    desabrig: Optional[float] = None
    desaloj: Optional[float] = None
    danos_prej_tot: Optional[float] = None
    
    # Monitoramento de desastres (CEMADEN)
    escola_risco: Optional[float] = None
    eventos_geohidro: Optional[float] = None
    pessoas_area_risco_cemaden: Optional[float] = None
    
    # TODO: Missing fields for : Áreas de risco

class MunicipalResilienceProfileReport(BaseModel):
    municipal_resilience_profile: MunicipalResilienceProfile
    
    @property
    def formatted_data_dict(self) -> Dict[str, Any]:
        data = self.municipal_resilience_profile.dict()
        for key, value in data.items():
            if value is None:
                data[key] = "—"
                continue
            
            if key in ["veg_natural", "agropec"]:
                data[key] = f"{CommonBusinessRules.brazilian_formatted_value(value)}% do município"                
            elif key in ["estiagem_incend", "geohidro", "tornad_vendav", "obitos", "desabrig", "desaloj"]:
                data[key] = CommonBusinessRules.brazilian_formatted_value_integer(value)
            elif key in ["danos_prej_tot"]:
                data[key] = CommonBusinessRules.brazilian_formatted_value_currency_short(value)
            elif key in ["escola_risco", "eventos_geohidro", "pessoas_area_risco_cemaden"]:
                data[key] = CommonBusinessRules.brazilian_formatted_value_integer(value)
                
        return data

    @property
    def formatted_data_df(self) -> pd.DataFrame:
        return pd.DataFrame([self.formatted_data_dict])
    
class ProjectInfo(BaseModel):
    name: str
    version: str
    description: str