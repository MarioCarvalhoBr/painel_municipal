# backend/src/domain/entities.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd

from ..helpers.common.formatting.number_formatting_processing import NumberFormattingProcessing

class County(BaseModel):
    county_id: int
    county: str
    state: str
    region: str
    display: Optional[str] = None
    
class CountyStatistics(BaseModel):
    id: Optional[int] = None
    county_id: Optional[int] = None
    gdp: Optional[float] = None
    area: Optional[float] = None
    idh: Optional[float] = None
    population: Optional[int] = None
    
    @property
    def formatted_area(self) -> Optional[str]:
        formatted_value = None
        if self.area is not None:
            truncated_value = NumberFormattingProcessing.to_decimal_truncated(self.area, value_to_ignore=None, precision=2)
            formatted_value = NumberFormattingProcessing.format_number_brazilian(float(truncated_value))
        return formatted_value
    
    @property
    def formatted_population(self) -> Optional[str]:
        formatted_value = None
        if self.population is not None:
            formatted_value = NumberFormattingProcessing.format_number_brazilian(self.population)
        return formatted_value

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
    future_value_color: Optional[str] = None
    imageurl: Optional[str] = None
    
    # Função estatic value_formatted para formatar em duas casas decimais e deixar no padrão brasileiro
    @staticmethod
    def format_value(value: Optional[float]) -> Optional[str]:
        if value is None:
            return None
        truncated_value = NumberFormattingProcessing.to_decimal_truncated(value, value_to_ignore=None, precision=2)
        brazilian_formatted_value = NumberFormattingProcessing.format_number_brazilian(float(truncated_value))
        
        return brazilian_formatted_value
    
    # criar uma property para current_value
    @property
    def formatted_current_value(self) -> Optional[str]:
        if self.current_value is None:
            return None
        return self.format_value(self.current_value)
    

    @property
    def formatted_future_value(self) -> Optional[str]:
        
        if self.current_value is None or self.future_value is None:
            return None
        
        result = self.current_value - self.future_value
        
        if result > 0:
            return f"+{self.format_value(result)}"
        elif result < 0:
            return f"-{self.format_value(abs(result))}"
        else:
            return "=0,00"
        
    

class RiskFactorReport(BaseModel):
    # Modificado para receber uma lista, já que precisamos agrupar vários itens
    risk_factors: List[RiskFactor]
        
    @property
    def formatted_data_dict(self) -> List[Dict[str, Any]]:
        """
        Retorna os dados agrupados como uma lista de dicionários,
        preservando a ordem do banco de dados.
        """
        agrupado = {}
        
        for rf in self.risk_factors:
            # Se é a primeira vez que vemos este risk_id, criamos a linha base
            if rf.risk_id not in agrupado:
                agrupado[rf.risk_id] = {
                    "risk_id": rf.risk_id,
                    "sep": rf.sep,
                    "risk": rf.risk,
                    "county": rf.county,
                    "state": rf.state,
                    "color": rf.color,
                    "imageurl": rf.imageurl,
                    
                    "current_value": rf.current_value,
                    "current_value_color": rf.current_value_color,
                    "formatted_current_value": rf.formatted_current_value,
                    
                    "future_value": rf.future_value,
                    "future_value_color": rf.future_value_color,
                    "formatted_future_value": rf.formatted_future_value,
                    
                    "Ameaça": "",
                    "Exposição": "",
                    "Vulnerabilidade": "",
                    "Sensibilidade": "",
                    "Capacidade adaptativa": ""
                }
            
            # Aqui fazemos a transposição: a string em 'detail' vira a chave (coluna),
            # e recebe o valor 'value'. 
            # Ex: agrupado[2]['Capacidade adaptativa'] = 0.38
            if rf.detail:
                # Opcional: Você pode querer normalizar a string (ex: title()) 
                # caso o banco traga variações de maiúsculas/minúsculas
                coluna_transposta = rf.detail.capitalize() if rf.detail.lower() == "capacidade adaptativa" else rf.detail
                agrupado[rf.risk_id][rf.detail] = rf.value
                
                agrupado[rf.risk_id][f"{rf.detail}_color"] = rf.color
                
        # Aplique a formatação brasileira para os valores numéricos format_value: Ameaça, Exposição, Vulnerabilidade, Sensibilidade, Capacidade adaptativa
        for key, item in agrupado.items():
            for col in ["Ameaça", "Exposição", "Vulnerabilidade", "Sensibilidade", "Capacidade adaptativa"]:
                if col in item and item[col] is not None:
                    item[col] = RiskFactor.format_value(item[col])
                
        # Retorna apenas os valores do dicionário (que será uma lista de dicionários na ordem original)
        return list(agrupado.values())

    @property
    def formatted_data_df(self) -> pd.DataFrame:
        """
        Retorna os dados no formato DataFrame do Pandas,
        mantendo a exata ordenação das linhas.
        """
        # O Pandas cria o DataFrame perfeitamente a partir de uma lista de dicionários
        return pd.DataFrame(self.formatted_data_dict)
    
    
    
    
    
class LegendItem(BaseModel):
    id: Optional[int] = None
    label: Optional[str] = None
    color: Optional[str] = None
    minvalue: Optional[float] = None
    maxvalue: Optional[float] = None
    legend_id: Optional[int] = None
    order: Optional[int] = None
    tag: Optional[str] = None


class PdfReportData(BaseModel):
    county_name: str
    state: str
    adaptation_data: List[County]

class ProjectInfo(BaseModel):
    name: str
    version: str
    description: str