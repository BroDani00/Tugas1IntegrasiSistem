from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Tugas 1 Integrasi Sistem",
    description="API Data Mahasiswa",
    version="1.0.0"
)


# =========================
# MODEL DATA
# =========================

class Item(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None


# =========================
# DATABASE SEMENTARA
# =========================

items_db = {}


# =========================
# ROOT
# =========================

@app.get("/")
def read_root():
    return {
        "message": "Selamat Datang di Tugas 1 Integrasi Sistem"
    }


# =========================
# CREATE - POST
# =========================

@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):

    if item_id in items_db:
        raise HTTPException(
            status_code=400,
            detail="Item already exists"
        )

    items_db[item_id] = item.model_dump()

    return {
        "message": "Item created successfully",
        "item": items_db[item_id]
    }


# =========================
# READ - GET
# =========================

@app.get("/items/{item_id}")
async def read_item(item_id: int):

    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "item": items_db[item_id]
    }


# =========================
# UPDATE - PUT
# =========================

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):

    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    items_db[item_id].update(
        item.model_dump(exclude_unset=True)
    )

    return {
        "message": "Item updated successfully",
        "item": items_db[item_id]
    }


# =========================
# DELETE
# =========================

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):

    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    deleted_item = items_db.pop(item_id)

    return {
        "message": "Item deleted successfully",
        "item": deleted_item
    }