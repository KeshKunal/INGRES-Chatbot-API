# In app/db.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

# Database setup
SQLALCHEMY_DATABASE_URL = settings.get_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def execute_query(filters: dict) -> list:
    """
    Safely builds and executes a SQL query on the "ingressdata2025" table.
    """
    # Use all relevant columns from the table
    query_builder = ['SELECT "STATES", "DISTRICT", "RainfallTotal", "AnnualGroundwaterRechargeTotal", "AnnualExtractableGroundwaterResourceTotal", "GroundWaterExtractionforAllUsesTotal", "StageofGroundWaterExtractionTotal", "NetAnnualGroundWaterAvailabilityforFutureUseTotal" FROM public."ingressdata2025" WHERE 1=1']
    params = {}

    # Dynamically and safely add filters from the JSON
    if 'state' in filters:
        query_builder.append('AND "STATES" ILIKE :state')
        params['state'] = f"%{filters['state']}%"

    if 'district' in filters:
        query_builder.append('AND "DISTRICT" ILIKE :district')
        params['district'] = f"%{filters['district']}%"
    
    # You can add more filters here for other columns as needed...

    final_query = " ".join(query_builder)

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
        query = "What is life"
        params={}
        # Execute with parameters
        result = session.execute(text(query), params)
        
        # Convert to dictionary list for easier handling
      #  columns = result.keys()
       # return [dict(zip(columns, row)) for row in result.fetchall()]