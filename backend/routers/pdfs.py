import crud

from uuid import uuid4
from typing import List
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import PDFRequest, PDFResponse
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File


router = APIRouter(prefix="/pdfs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=PDFResponse, status_code=status.HTTP_201_CREATED)
def create_pdf(pdf: PDFRequest, db: Session = Depends(get_db)):
    return crud.create_pdf(db, pdf)

@router.post("/upload", response_model=PDFResponse, status_code=status.HTTP_201_CREATED)
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    print("File::: ", file)
    file_name = f"{uuid4()}-{file.filename}"
    print("FileName::: ", file_name)
    return crud.upload_pdf(db, file, file_name)

@router.get("", response_model=List[PDFResponse])
def get_pdfs(selected: bool = None, db: Session = Depends(get_db)):
    return crud.read_pdfs(db, selected)

@router.get("/{id}", response_model=PDFResponse)
def get_pdfs(id: int, db: Session = Depends(get_db)):
    pdf = crud.read_pdf(db, id)
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return pdf

@router.put("/{id}", response_model=PDFResponse)
def get_pdfs(id: int, pdf: PDFRequest, db: Session = Depends(get_db)):
    updated_pdf = crud.update_pdf(db, id, pdf)
    if updated_pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return updated_pdf

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_pdf(id: int, db: Session = Depends(get_db)):
    res = crud.delete_pdf(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return {"message": "PDF successfully deleted"}