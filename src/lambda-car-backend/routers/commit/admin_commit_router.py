from uuid import UUID
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from openpyxl import load_workbook

from commands.commit_commands import (
    CreateCommitCommand,
    UpdateCommitCommand,
    ImportCommitItemCommand,
    ImportCommitsCommand,
)
from dependencies import get_commit_service, require_admin
from schemas.commit_schemas import (
    CreateCommitRequest,
    UpdateCommitRequest,
    CommitResponse,
    ImportCommitsResponse,
)
from services.commit_service import CommitService


router = APIRouter(prefix="/admin/commits", tags=["admin-commits"])


@router.post("/", response_model=CommitResponse, status_code=status.HTTP_201_CREATED)
def create_commit(
    payload: CreateCommitRequest,
    admin_id: UUID = Depends(require_admin),
    service: CommitService = Depends(get_commit_service),
):
    try:
        commit = service.create_commit(
            CreateCommitCommand(
                code=payload.code,
                description=payload.description,
            )
        )
        return CommitResponse.from_domain(commit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{commit_id}", response_model=CommitResponse)
def get_commit(
    commit_id: UUID,
    admin_id: UUID = Depends(require_admin),
    service: CommitService = Depends(get_commit_service),
):
    try:
        commit = service.get_commit(commit_id)
        return CommitResponse.from_domain(commit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{commit_id}", response_model=CommitResponse)
def update_commit(
    commit_id: UUID,
    payload: UpdateCommitRequest,
    admin_id: UUID = Depends(require_admin),
    service: CommitService = Depends(get_commit_service),
):
    try:
        commit = service.update_commit(
            UpdateCommitCommand(
                commit_id=commit_id,
                code=payload.code,
                description=payload.description,
            )
        )
        return CommitResponse.from_domain(commit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{commit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commit(
    commit_id: UUID,
    admin_id: UUID = Depends(require_admin),
    service: CommitService = Depends(get_commit_service),
):
    try:
        service.delete_commit(commit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/import-excel",
    response_model=ImportCommitsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def import_commits_excel(
    file: UploadFile = File(...),
    admin_id: UUID = Depends(require_admin),
    service: CommitService = Depends(get_commit_service),
):
    filename = file.filename or ""

    if not filename.endswith((".xlsx", ".xlsm")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .xlsx or .xlsm files are supported",
        )

    try:
        content = await file.read()
        workbook = load_workbook(filename=BytesIO(content), data_only=True)
        sheet = workbook.active

        items: list[ImportCommitItemCommand] = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if len(row) < 2:
                continue

            code = row[0]
            description = row[1]

            if code is None and description is None:
                continue

            items.append(
                ImportCommitItemCommand(
                    code=str(code or "").strip(),
                    description=str(description or "").strip(),
                )
            )

        result = service.import_commits(ImportCommitsCommand(items=items))
        return ImportCommitsResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))