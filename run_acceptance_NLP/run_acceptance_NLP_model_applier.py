import joblib
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

model_path = r"C:\Users\SSagynov\python_exp\run_acceptance_NLP\lgs_email_classifier_model.pkl"
vectorizer_path = r"C:\Users\SSagynov\python_exp\run_acceptance_NLP\tfidf_vectorizer.pkl"

loaded_model = joblib.load(model_path)
loaded_vectorizer = joblib.load(vectorizer_path)

def preprocess_input_text(text, stop_words):
    text = text.lower()  
    words = text.split()
    words = [word for word in words if word.isalnum() and word not in stop_words]  
    return ' '.join(words)

def predict_email_category(user_input):
   
    preprocessed_text = preprocess_input_text(user_input, stop_words)
    text_tfidf = loaded_vectorizer.transform([preprocessed_text])
    
    prediction = loaded_model.predict(text_tfidf)
    return prediction[0]

if __name__ == "__main__":
    print("Email Classifier - Type 'exit' to quit.")
    while True:
        user_input = input("Enter the email content: ")
        
        if user_input.lower() == 'exit':
            print("Exiting the Email Classifier.")
            break
        
        if ('distance' not in user_input.lower() and 'agm' not in user_input.lower()) or len(user_input) < 30:
            print("Invalid input! The text must contain 'distance adaptation statement (if appicable)' or 'number of AGM' and have at least 30 characters.")
            continue  
        
        predicted_category = predict_email_category(user_input)
                
        if predicted_category==1:
            print(f"The run is classified as: accepted")
        else:
            print(f"The run is classified as: not accepted")



