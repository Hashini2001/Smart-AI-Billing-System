import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, regularizers
import os
import json

# Path to your image dataset
train_dir = 'images/Train'
validation_dir = 'images/Validation'

# Check if the train and validation directories exist
if not os.path.exists(train_dir) or not os.path.exists(validation_dir):
    raise FileNotFoundError("Train or validation directory not found. Please check the paths.")

# ImageDataGenerator to load and preprocess images
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

# Load images from directories
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),  
    batch_size=16,  
    class_mode='binary' if len(os.listdir(train_dir)) == 2 else 'categorical',
    shuffle=True  
)
validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(128, 128),  
    batch_size=16,  
    class_mode='binary' if len(os.listdir(validation_dir)) == 2 else 'categorical',
    shuffle=False  
)

# Get class indices and save them to a JSON file for later use
class_indices = train_generator.class_indices
print(class_indices)  # Print class indices to verify

# Save the class indices to a JSON file
with open('class_indices.json', 'w') as json_file:
    json.dump(class_indices, json_file)

# model for binary or multi-class classification
output_units = 1 if train_generator.class_mode == 'binary' else train_generator.num_classes
output_activation = 'sigmoid' if train_generator.class_mode == 'binary' else 'softmax'
loss_function='binary_crossentropy' if train_generator.class_mode=='binary' else 'categorical_crossentropy'

# model with reduced complexity
model = models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=(128, 128, 3), 
                  kernel_regularizer=regularizers.l2(0.01)),  # Reduced filters
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.3),  # dropout layer
    
    layers.Conv2D(32, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.01)),  
    # Reduced filters
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.3),  # dropout layer
    
    layers.Conv2D(64, (3, 3), activation='relu', kernel_regularizer=regularizers.l2(0.01)),  
    # Reduced filters
    layers.MaxPooling2D(2, 2),
    layers.Dropout(0.3),  # dropout layer

    layers.Flatten(),
    layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.01)),  
    # Reduced units
    layers.Dropout(0.5),  # dropout layer
    layers.Dense(output_units, activation=output_activation)  # Output layer
])

# Compile the model
model.compile(optimizer='adam',
              loss=loss_function,
              metrics=['accuracy'])

# Train the model with early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',  # Monitor validation loss
    patience=10,  # Stop after 10 epochs with no improvement
    restore_best_weights=True  # Restore weights from the best epoch
)

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=25,  
    verbose=1,  # training progress
    callbacks=[early_stopping]  #early stopping
)

# Print training and validation accuracy
print("Training Accuracy:", history.history['accuracy'][-1])
print("Validation Accuracy:", history.history['val_accuracy'][-1])

# Save the trained model for later use
model.save('item_classifier.h5')

# Print success message
print("AI model trained successfully and saved as 'item_classifier.h5'")