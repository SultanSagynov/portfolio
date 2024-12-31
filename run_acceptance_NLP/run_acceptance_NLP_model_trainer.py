import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import joblib


df = pd.read_csv(r"C:\Users\SSagynov\python_exp\run_acceptance_NLP\messages_filtered.csv")
df['Filtered_message'] = df['Filtered_message'].fillna('').apply(lambda x: x.lower() if isinstance(x, str) else str(x))

stop_words = set(stopwords.words('english'))

def preprocess_email(text):
    text = text.lower()  
    words = text.split()  
    words = [word for word in words if word.isalnum() and word not in stop_words]  
    return ' '.join(words)

df['processed_content'] = df['Filtered_message'].apply(preprocess_email)

X = df['processed_content']
y = df['Decision']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

lr_model = LogisticRegression(max_iter=1000)

lr_model.fit(X_train_tfidf, y_train)

lr_cv_scores = cross_val_score(lr_model, X_train_tfidf, y_train, cv=5, scoring='accuracy')

y_pred_lr = lr_model.predict(X_test_tfidf)

print("Logistic Regression Classification Report:")
print(classification_report(y_test, y_pred_lr))

print("Logistic Regression Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_lr))

print(f'Logistic Regression Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}')

fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_model.predict_proba(X_test_tfidf)[:, 1])

plt.figure(figsize=(10, 6))
plt.plot(fpr_lr, tpr_lr, color='green', label=f'Logistic Regression (AUC = {auc(fpr_lr, tpr_lr):.2f})')
plt.plot([0, 1], [0, 1], color='red', linestyle='--', label='Random Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

joblib.dump(lr_model, r"C:\Users\SSagynov\python_exp\run_acceptance_NLP\lgs_email_classifier_model.pkl")
joblib.dump(vectorizer, r"C:\Users\SSagynov\python_exp\run_acceptance_NLP\tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully!")
