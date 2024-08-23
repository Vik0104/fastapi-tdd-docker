from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema, SummaryUpdatePayloadSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    response_object = {"id": summary_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int = Path(..., gt=0)):
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[int]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(id: int) -> SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(id)

    return summary

# @router.put("/{id}/", response_model=SummarySchema)
# async def update_summary(id: int, payload: SummaryUpdatePayloadSchema):
#     summary = await crud.put(id, payload)
#     if not summary:
#         raise HTTPException(status_code=404, detail="Summary not found")

#     return summary

@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(id: int, payload: SummaryUpdatePayloadSchema):
    try:
        summary = await crud.put(id, payload)
        if not summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        return summary
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))