# tunnel-image-recognition

# Tunnel Displacement Analysis using Machine Learning

## Overview

This project is an **image recognition system** designed to read and analyze **tunnel design graphical outputs**, specifically **displacement contour plots**. By leveraging machine learning, the system automates the extraction of displacement values (e.g., at the **crown** and **sidewalls**) from these graphical outputs. The goal is to **save time, reduce manual errors, and streamline engineering reporting**.

## Objectives

- Develop a **machine learning-based system** using TensorFlow to process **displacement contour plots**.
- Extract key displacement values such as **maximum displacements** at the **crown and sidewalls**.
- Automatically **tabulate** the extracted results for seamless integration into engineering reports.

## Technical Approach

### 1. Data Preparation
- **Dataset:** Collect and annotate displacement contour plot images with corresponding displacement values.
- **Annotations:** Label the **crown** and **sidewall** regions for precise extraction of displacement values.
- **Preprocessing:** Normalize images and apply **noise reduction** techniques to enhance data quality.

### 2. Model Architecture
- **Feature Extraction:** Utilize **Convolutional Neural Networks (CNNs)** to identify **regions of interest** (e.g., crown and sidewalls) and extract relevant features.
- **Regression Layer:** Implement **regression layers** for predicting numerical displacement values.
- **Tools:** Leverage **TensorFlow/Keras** for model development and training.

### 3. Training and Validation
- **Loss Function:** Use **Mean Squared Error (MSE)** for optimizing numerical predictions.
- **Evaluation Metrics:** Validate model accuracy using **Mean Absolute Error (MAE)** and **R² score**.
- **Augmentation:** Apply techniques such as **rotation** and **scaling** to improve generalization.

### 4. Prediction Pipeline
- **Input Handling:** Accept **numerical contour plot images** and preprocess them for model compatibility.
- **Inference:** Pass processed images through the trained model to **extract displacement values**.
- **Output:** Generate a structured output containing **predicted displacements** for the **crown and sidewalls**.

### 5. Integration and Automation
- **Automate the prediction pipeline** for **real-time usage**.
- **Develop a tabulation script** to compile **displacement values into engineering reports**.

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- **Python 3.8+**
- **TensorFlow/Keras**
- **OpenCV**
- **NumPy**
- **Matplotlib**
- **Pandas**

### Setup
Clone this repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/tunnel-displacement-ml.git
cd tunnel-displacement-ml

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

'''

# Usage

## Train the Model
To train the displacement extraction model, use the following command:

```bash
python train.py --data_path ./data
```

## Predict Displacement Values
To run inference on a displacement contour plot:

```bash
python predict.py --image_path ./test_images/sample.png
```

## Generate Report
To automate the tabulation of extracted values into a structured report:

```bash
python generate_report.py --results_path ./results
```

# Benefits
- **Efficiency:** Automates displacement analysis, significantly reducing manual effort.
- **Accuracy:** Leverages machine learning to minimize errors in value extraction.
- **Scalability:** Adaptable to various tunnel geometries and displacement ranges.
- **Consistency:** Ensures standardized output across multiple projects.

# Contributing
We welcome contributions to enhance this project. Please follow these steps:

```bash
# Fork the repository
git checkout -b feature-name

# Commit changes
git commit -m "Add new feature"

# Push to the branch
git push origin feature-name
```

Open a **pull request** to merge your changes.

