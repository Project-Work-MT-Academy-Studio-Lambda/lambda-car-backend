from fastapi import APIRouter, Depends, HTTPException, status

from ...dependencies import get_commit_service, require_user
from ...schemas.commit_schemas import CommitResponse
from ...services.commit_service import CommitService
from ...logger import get_logger

from ...domain.user import CurrentUser

router = APIRouter(prefix="/commits", tags=["commits"])
logger = get_logger(__name__)

@router.get("/", response_model=list[CommitResponse], status_code=status.HTTP_200_OK)
def list_commits(
    current_user: CurrentUser = Depends(require_user),
    service: CommitService = Depends(get_commit_service),
):
    logger.debug(f"User {current_user.id} is listing backlog commits")
    try:
        commits = service.find_backlog_commits()
        return [CommitResponse.from_domain(commit) for commit in commits]
    except ValueError as e:
        logger.error(f"Error occurred while fetching commits: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))