import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# 初始化
def init_firebase():
    cred = credentials.Certificate('python-test-712c8-firebase-adminsdk-ar8rj-20a1dd07ca.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


# 增
def firebase_add(db, path, data):
    doc_ref = db.document(path)
    doc_ref.set(data)


# 刪
def firebase_delete(db, path):
    doc_ref = db.document(path)
    doc_ref.delete()


# 改
def firebase_update(db, path, data):
    doc_ref = db.document(path)
    doc_ref.update(data)


# 查
def firebase_read(db, path):
    doc_ref = db.document(path)
    try:
        doc = doc_ref.get()
        return doc.to_dict()
    except():
        print("指定文件不存在，請檢查路徑是否正確")
        return 0

