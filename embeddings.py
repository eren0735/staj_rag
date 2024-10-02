from pymilvus import connections, CollectionSchema, FieldSchema, DataType, utility

def initialize_milvus():
    # Mevcut bağlantıyı kontrol et
    connection_alias = "default"
    if connection_alias in connections.list_connections():
        try:
            # Bağlantıyı kapat
            connections.disconnect(connection_alias)
            print(f"'{connection_alias}' bağlantısı kapatıldı.")
        except Exception as e:
            print(f"Bağlantı kapatma hatası: {str(e)}")

    # Milvus'a bağlan
    try:
        connections.connect(connection_alias, host='localhost', port='19530')
        print("Milvus'a bağlanıldı.")
    except Exception as e:
        print(f"Bağlantı hatası: {str(e)}")
        return

    # Koleksiyon şemasını tanımlayın
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128)  # Vektör boyutunu belirtin
    ]
    schema = CollectionSchema(fields=fields, description="Blog koleksiyonu")

    # Koleksiyonu oluştur
    collection_name = "blogs_collection"
    
    # Koleksiyon zaten var mı kontrol et
    if utility.has_collection(collection_name):
        print(f"Koleksiyon '{collection_name}' zaten mevcut.")
    else:
        # Koleksiyonu oluştur
        try:
            collection = utility.create_collection(collection_name, schema)
            print(f"Koleksiyon '{collection_name}' başarıyla oluşturuldu.")
        except Exception as e:
            print(f"Koleksiyon oluşturma hatası: {str(e)}")

# Fonksiyonu çağır
if __name__ == "__main__":
    initialize_milvus()
