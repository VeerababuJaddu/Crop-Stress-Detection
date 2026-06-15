import os
from django.conf import settings
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

def create_data_generators(train_dir, validation_dir, test_dir, img_size=224, batch_size=32):
    """Create ImageDataGenerators for training, validation, and testing."""
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,  # Normalize pixel values between 0 and 1
        rotation_range=20,  # Augment images with slight rotation
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
    )

    validation_datagen = ImageDataGenerator(rescale=1.0 / 255)
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode="categorical",
    )

    validation_gen = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode="categorical",
    )

    test_gen = test_datagen.flow_from_directory(
        test_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=False,
    )

    return train_gen, validation_gen, test_gen

def build_cnn_model(img_size=224, num_classes=2):
    """Build the CNN model."""
    model = Sequential([
        Conv2D(32, (3, 3), activation="relu", input_shape=(img_size, img_size, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation="relu"),
        MaxPooling2D(2, 2),
        Conv2D(256, (3, 3), activation="relu"),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation="relu"),
        Dropout(0.5),
        Dense(num_classes, activation="softmax"),
    ])
    return model

def compile_and_train_model(model, train_gen, validation_gen, epochs=40):
    """Compile and train the model with callbacks."""
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    # Callbacks
    early_stopping = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=3, min_lr=1e-6)

    history = model.fit(
        train_gen,
        validation_data=validation_gen,
        epochs=epochs,
        callbacks=[early_stopping, reduce_lr],
    )
    
    return model, history

def evaluate_and_visualize(model, test_gen, history):
    """Evaluate the model and visualize results."""
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(test_gen)
    print(f"\nTest Loss: {test_loss:.3f}")
    print(f"Test Accuracy: {test_accuracy:.3f}")

    # Plot accuracy and loss curves
    acc = history.history["accuracy"]
    val_acc = history.history["val_accuracy"]
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    epochs_range = range(len(acc))

    plt.figure()
    plt.plot(epochs_range, acc, label="Training Accuracy")
    plt.plot(epochs_range, val_acc, label="Validation Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.legend()

    plt.figure()
    plt.plot(epochs_range, loss, label="Training Loss")
    plt.plot(epochs_range, val_loss, label="Validation Loss")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.show()

def generate_confusion_matrix(model, test_gen):
    """Generate confusion matrix and classification report."""
    predictions = model.predict(test_gen)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = test_gen.classes
    class_labels = list(test_gen.class_indices.keys())

    conf_matrix = confusion_matrix(true_classes, predicted_classes)
    disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=class_labels)
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.show()

    print("\nClassification Report:")
    print(classification_report(true_classes, predicted_classes, target_names=class_labels))

def Classification_report(img_size=224, batch_size=32, epochs=40):
   # Dynamically using settings.MEDIA_ROOT for flexibility
    train_dir = os.path.join(settings.MEDIA_ROOT, 'Dataset', 'train')
    validation_dir = os.path.join(settings.MEDIA_ROOT, 'Dataset', 'validation')
    test_dir = os.path.join(settings.MEDIA_ROOT, 'Dataset', 'test')
    model_save_path = os.path.join(settings.MEDIA_ROOT, 'Dataset', 'crop_stress_model.h5')
    # Step 1: Prepare data generators
    train_gen, validation_gen, test_gen = create_data_generators(train_dir, validation_dir, test_dir, img_size, batch_size)

    # Display class indices
    print("\nClass indices:", train_gen.class_indices)

    # Step 2: Build and compile the model
    model = build_cnn_model(img_size, len(train_gen.class_indices))

    # Print the model summary
    model.summary()

    # Step 3: Train the model
    model, history = compile_and_train_model(model, train_gen, validation_gen, epochs)

    # Step 4: Save the model
    if model_save_path:
        model.save(model_save_path)
        print(f"\nModel saved at {model_save_path}")

    # Step 5: Evaluate and visualize the results
    evaluate_and_visualize(model, test_gen, history)

    # Step 6: Generate confusion matrix and classification report
    generate_confusion_matrix(model, test_gen)

    accuracy= model.evaluate(test_gen)[1]  # Return test accuracy

    return accuracy





