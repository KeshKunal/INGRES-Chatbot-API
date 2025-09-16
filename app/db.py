# app/db.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        
def execute_query(filters):
    """Execute query based on filters from LLM"""
    with SessionLocal() as session:
        """
        # Start with base query
        query = "always refer to the table name as public.ingressdata2025. The list of table columns are as follows: SNo, STATES, DISTRICT, RainfallC, RainfallNC, RainfallPQ, RainfallTotal, RechargeAreaC, RechargeAreaNC, RechargeAreaPQ, RechargeAreaTotal, Hilly_Area, TotalArea, RainfallRechargeC, RainfallRechargeNC, RainfallRechargePQ, RainfallRechargeTotal, CanalsC, CanalsNC, CanalsPQ, CanalsTotal, SurfaceWaterIrrigationC, SurfaceWaterIrrigationNC, SurfaceWaterIrrigationPQ," #SurfaceWaterIrrigationTotal, GroundWaterIrrigationC, GroundWaterIrrigationNC, GroundWaterIrrigationPQ, GroundWaterIrrigationTotal, TanksandPondsC, TanksandPondsNC, TanksandPondsPQ, TanksandPondsTotal, WaterConservationStructureC, WaterConservationStructureNC, WaterConservationStructurePQ, WaterConservationStructureTotal, PipelinesC, PipelinesNC, PipelinesPQ, PipelinesTotal, SewagesandFlashFloodChannelsC, SewagesandFlashFloodChannelsNC, SewagesandFlashFloodChannelsPQ, SewagesandFlashFloodChannelsTotal, GroundWaterRecharge_ham_C, GroundWaterRechargeNC, GroundWaterRechargePQ, GroundWaterRechargeTotal, BaseFlowC, BaseFlowNC, BaseFlowPQ, BaseFlowTotal, StreamRechargesC, StreamRechargesNC, StreamRechargesPQ, StreamRechargesTotal, LateralFlowsC, LateralFlowsNC, LateralFlowsPQ, LateralFlowsTotal, VerticalFlowsC, VerticalFlowsNC, VerticalFlowsPQ, VerticalFlowsTotal, EvaporationC, EvaporationNC, EvaporationPQ, EvaporationTotal, TranspirationC, TranspirationNC, TranspirationPQ, TranspirationTotal, EvapotranspirationC, EvapotranspirationNC, EvapotranspirationPQ, EvapotranspirationTotal, InFlowsAndOutFlowsC, InFlowsAndOutFlowsNC, InFlowsAndOutFlowsPQ, InFlowsAndOutFlowsTotal, AnnualGroundwaterRechargeC, AnnualGroundwaterRechargeNC, AnnualGroundwaterRechargePQ, AnnualGroundwaterRechargeTotal, EnvironmentalFlowsC, EnvironmentalFlowsNC, EnvironmentalFlowsPQ, EnvironmentalFlowsTotal, AnnualExtractableGroundwaterResourceC, AnnualExtractableGroundwaterResourceNC, AnnualExtractableGroundwaterResourcePQ, AnnualExtractableGroundwaterResourceTotal, GroundWaterExtractionforDomesticUsesC, GroundWaterExtractionforDomesticUsesNC, GroundWaterExtractionforDomesticUsesPQ, GroundWaterExtractionforDomesticUsesTotal, GroundWaterExtractionforIndustrialUsesC, GroundWaterExtractionforIndustrialUsesNC, GroundWaterExtractionforIndustrialUsesPQ, GroundWaterExtractionforIndustrialUsesTotal, GroundWaterExtractionforIrrigationUsesC, GroundWaterExtractionforIrrigationUsesNC, GroundWaterExtractionforIrrigationUsesPQ, GroundWaterExtractionforIrrigationUsesTotal, GroundWaterExtractionforAllUsesC, GroundWaterExtractionforAllUsesNC, GroundWaterExtractionforAllUsesPQ, GroundWaterExtractionforAllUsesTotal, StageofGroundWaterExtractionC, StageofGroundWaterExtractionNC, StageofGroundWaterExtractionPQ, StageofGroundWaterExtractionTotal, AllocationofGroundWaterResourceforDomesticUtilisationC, AllocationofGroundWaterResourceforDomesticUtilisationNC, AllocationofGroundWaterResourceforDomesticUtilisationPQ, AllocationofGroundWaterResourceforDomesticUtilisationTotal, NetAnnualGroundWaterAvailabilityforFutureUseC, NetAnnualGroundWaterAvailabilityforFutureUseNC, NetAnnualGroundWaterAvailabilityforFutureUsePQ, NetAnnualGroundWaterAvailabilityforFutureUseTotal, WaterloggedandshallowwaterTable, FloodProne, SpringDischarge, FreshInStorageUnconfinedGroundWaterResources, SalineInStorageUnconfinedGroundWaterResources, FreshTotalGroundWaterAvailabilityinUnconfinedAquifier, SalineTotalGroundWaterAvailabilityinUnconfinedAquifier, FreshDynamicConfinedGroundWaterResources, SalineDynamicConfinedGroundWaterResources, FreshInStorageConfinedGroundWaterResources, SalineInStorageConfinedGroundWaterResources, FreshTotalConfinedGroundWaterResources, SalineTotalConfinedGroundWaterResources, FreshDynamicSemiConfinedGroundWaterResources, SalineDynamicSemiConfinedGroundWaterResources, FreshInStorageSemiConfinedGroundWaterResources, SalineInStorageSemiConfinedGroundWaterResources, FreshTotalSemiConfinedGroundWaterResources, SalineTotalSemiConfinedGroundWaterResources, FreshTotalGroundWaterAvailabilityinthearea, SalineTotalGroundWaterAvailabilityinthearea"
        query += "SELECT * FROM groundwater_data WHERE 1=1"
        params = {}
        
        # Add filters dynamically
        if 'assessment_unit' in filters:
            query += " AND assessment_unit ILIKE :assessment_unit"
            params['assessment_unit'] = f"%{filters['assessment_unit']}%"
            
        if 'year' in filters:
            query += " AND year = :year"
            params['year'] = filters['year']
        """
        query = ""
        params={}
        # Execute with parameters
        result = session.execute(text(query), params)
        
        # Convert to dictionary list for easier handling
      #  columns = result.keys()
       # return [dict(zip(columns, row)) for row in result.fetchall()]