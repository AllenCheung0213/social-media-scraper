import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

column_names = ["target", "id", "date", "flag", "user", "text"]

df = pd.read_csv("training.1600000.processed.noemoticon.csv", encoding="ISO-8859-1", names=column_names)

df['text'] = df['text'].str.lower()

unique_classes = df['target'].unique()
class_weights = compute_class_weight(class_weight='balanced', classes=unique_classes, y=df['target'])
class_weight_dict = dict(zip(unique_classes, class_weights))

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['target'], test_size=0.2, random_state=42)

# Create a pipeline with TF-IDF vectorizer and Logistic Regression classifier
model = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression(class_weight=class_weight_dict)
)

# Train the model
model.fit(X_train, y_train)

# Predict the sentiment on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))