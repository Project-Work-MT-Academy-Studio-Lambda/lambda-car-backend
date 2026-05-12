from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from ...logger import get_logger
from ...dependencies import require_admin, get_export_service
from ...services.operations.export_service import ExportService

router = APIRouter(
    prefix="/admin/export/excel",
    tags=["admin_excel"],
)

logger = get_logger(__name__)


@router.get("/", status_code=status.HTTP_200_OK)
def export_data_to_excel(
    service: ExportService = Depends(get_export_service),
    current_user=Depends(require_admin),
):
    logger.debug(f"Admin user {current_user.id} is exporting data to excel")

    try:
        excel_bytes = service.export_data()

        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": 'attachment; filename="lambdacar_export.xlsx"'
            },
        )

    except ValueError as e:
        logger.error(f"Error occurred while exporting data to Excel: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )