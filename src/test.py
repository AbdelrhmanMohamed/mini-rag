# استيراد المكتبات
from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

import os

# 1. تحميل ملف PDF
loader = PyPDFLoader("cv.pdf")  # ضع اسم ملفك هنا
documents = loader.load()

# 2. تقسيم النص إلى مقاطع صغيرة
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 3. إنشاء التمثيلات الرقمية (Embeddings) باستخدام نموذج مجاني
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. بناء قاعدة بيانات FAISS
vectorstore = FAISS.from_documents(docs, embedding_model)

# 5. استخدام LLM مجاني من HuggingFace
# سنستخدم نموذج بسيط عبر HuggingFaceHub (تحتاج حساب مجاني HuggingFace Token) أو نحمل موديل محلي.
# ولكن هنا سأعتمد موديل بسيط محلي عبر langchain.llms


# إنشاء Pipeline محلي للإجابة على الأسئلة
qa_pipeline = pipeline(
    "text-generation",
    model="gpt2",     # أو يمكنك اختيار نموذج أكبر لو أردت
    max_new_tokens=200,
    temperature=0.5
)

llm = HuggingFacePipeline(pipeline=qa_pipeline)

# 6. بناء سلسلة استرجاع وإجابة
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# 7. تجربة النظام
while True:
    query = input("\n📝 اكتب سؤالك (أو اكتب 'خروج' للخروج): ")
    if query.lower() == "خروج":
        break
    result = qa_chain.run(query)
    print(f"\n✅ الإجابة: {result}\n")
