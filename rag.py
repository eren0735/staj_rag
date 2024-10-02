from fastapi import FastAPI, HTTPException, APIRouter
import numpy as np
from sentence_transformers import SentenceTransformer
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from pymilvus import connections
# FastAPI uygulaması oluştur
app = FastAPI()
router = APIRouter()

# Milvus sunucusuna bağlan
from pymilvus import connections

# Milvus sunucusuna bağlan
from pymilvus import utility

def connect_to_milvus():
    existing_connections = connections.list_connections()
    if "default" not in existing_connections:
        connections.connect("default", host="127.0.0.1", port="19530")
        print("Milvus sunucusuna başarıyla bağlanıldı.")
    else:
        print("Milvus zaten bağlı.")


# Bağlantıyı oluştur
connect_to_milvus()

# Embedding için kullanılan SentenceTransformer modeli
model = SentenceTransformer('all-MiniLM-L6-v2')

# Blog vektörleri için Milvus koleksiyonu
collection_name = "blogs_collection"

# Koleksiyonu oluşturma ve indeks kontrolü
def create_blog_collection():
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)  # 384 boyutlu vektör
    ]
    schema = CollectionSchema(fields, description="Blog vektör koleksiyonu")

    # Koleksiyonu kontrol et ve oluştur
    if not utility.has_collection(collection_name):
        collection = Collection(collection_name, schema)
        print(f"Koleksiyon '{collection_name}' başarıyla oluşturuldu.")
    else:
        collection = Collection(collection_name)
        print(f"Koleksiyon '{collection_name}' zaten mevcut.")

    # İndeksi kontrol et
    index_list = collection.indexes
    if len(index_list) == 0:
        index_params = {
            "index_type": "IVF_FLAT",  # İndeks türü
            "metric_type": "L2",  # Benzerlik ölçütü
            "params": {"nlist": 128}  # nlist parametresi
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        print(f"İndeks '{collection_name}' koleksiyonu için oluşturuldu.")
    else:
        print(f"Koleksiyon '{collection_name}' için indeks zaten mevcut.")

    return collection

# Koleksiyonu oluştur
collection = create_blog_collection()

# Sorgu için Milvus'u kullanarak benzer blogları bulma
def search_similar_blogs(query: str, top_k: int = 5):
    if collection is None:
        raise RuntimeError("Koleksiyon henüz oluşturulmadı.")

    print(f"Sorgu: {query}")  # Sorguyu yazdır
    query_embedding = model.encode([query])  # Sorgu için embedding oluştur
    query_embedding = np.array(query_embedding, dtype=np.float32)

    # Arama işlemi
    collection.load()
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(query_embedding.tolist(), "embedding", search_params, limit=top_k)

    # Sonuçları kontrol et
    if len(results[0]) == 0:
        print("Sonuç bulunamadı.")  # Bulunamadıysa ekrana yazdır
        return [], "Sonuç bulunamadı."
    
    print("Sonuç bulundu.")  # Sonuç varsa ekrana yazdır
    # En benzer blog ID'lerini döner
    return [hit.entity.id for hit in results[0]], "Sonuç bulundu."

# Tüm blogları almak için bir endpoint
@router.get("/blogs/")
async def get_blogs():
    if collection is None:
        raise RuntimeError("Koleksiyon henüz oluşturulmadı.")

    # Tüm blogları alma işlemi
    collection.load()
    results = collection.query(expr="*", limit=100)  # Tüm blogları getir, limit 100

    # Blog verilerini döner
    return {"blogs": results}

# Arama endpoint'i
@router.get("/search/")
async def search(query: str, top_k: int = 5):
    try:
        search_results, message = search_similar_blogs(query, top_k)
        return {"message": message, "results": search_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Router'ı FastAPI uygulamasına ekle
app.include_router(router)

