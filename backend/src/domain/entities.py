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
    
    @staticmethod
    def format_value(value: Optional[float]) -> Optional[str]:
        if value is None:
            return None
        truncated_value = NumberFormattingProcessing.to_decimal_truncated(value, value_to_ignore=None, precision=2)
        brazilian_formatted_value = NumberFormattingProcessing.format_number_brazilian(float(truncated_value))
        
        return brazilian_formatted_value
        

class RiskFactorReport(BaseModel):
    risk_factors: List[RiskFactor]
        
    @property
    def formatted_data_dict(self) -> List[Dict[str, Any]]:
        grouped_risks = {}
        
        for rf in self.risk_factors:
            if rf.risk_id not in grouped_risks:
                grouped_risks[rf.risk_id] = {
                    "risk_id": rf.risk_id,
                    "sep": rf.sep,
                    "risk": rf.risk,
                    "county": rf.county,
                    "state": rf.state,
                    "color": rf.color,
                    "imageurl": rf.imageurl,
                    
                    "current_value": rf.current_value,
                    "current_value_color": rf.current_value_color,
                    "formatted_current_value": RiskFactor.format_value(rf.current_value),
                    
                    "future_value": rf.future_value,
                    "future_value_color": rf.future_value_color,
                    "formatted_future_value": RiskFactor.format_value(rf.future_value),
                    
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
                    item[col] = RiskFactor.format_value(item[col])
                
        return list(grouped_risks.values())

    @property
    def formatted_data_df(self) -> pd.DataFrame:
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