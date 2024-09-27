# Wireless and Mobile Networks Calculator 📡

### Description
This project is a handy tool for calculating various metrics essential in wireless and mobile networks. It supports calculations for sampler and interleaver configurations, OFDM parameters, power transmission, throughput, and cellular system design. Each module integrates specific formulas and considerations unique to telecommunications, making it an invaluable educational and professional resource.

### Key Features:
- **Dynamic Form Fields**: Depending on the selected calculation type, the app dynamically generates the necessary input fields, showcasing advanced DOM manipulation. 📝
- **Asynchronous JavaScript**: Uses `async` and `await` for making asynchronous requests to the server, ensuring the UI remains responsive. ⚡
- **Flask Server**: Utilizes Flask for the backend to handle API requests and serve the application, demonstrating how Python can be used in server-side development. 🐍
- **Data Handling**: Temporarily stores input data on the server to process calculations, highlighting server-side data management. 💾

### Programming Languages and Tools:

<img align="left" alt="HTML5" width="50px" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" />
<img align="left" alt="CSS3" width="50px" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" />
<img align="left" alt="JavaScript" width="50px" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" />
<img align="left" alt="Python" width="50px" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" />
<img align="left" alt="Flask" width="50px" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/flask/flask-original.svg" />
<img align="left" alt="PyCharm" width="50px" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pycharm/pycharm-original.svg"/><br><br>

### Setup and Installation
Ensure you have Python and Node.js installed on your system to set up and run this project.
- Navigate to the project directory:
  ```bash
  cd Wireless
  ```
- Install Python dependencies:
  ```bash
  pip install flask flask-cors
  ```
- Start the Flask server:
  ```bash
  python app.py
  ```

### How to Use
- Open your web browser and go to [http://localhost:5000/](http://localhost:5000/) to access the calculator. 🌐
- Select the desired calculation type from the dropdown menu and fill in the required input fields. 📋
- Click the "Calculate" button to see the results. 📊

### Calculation Types:
- **Sampler and Interleaver**: Enter parameters like bandwidth, number of bits per sample, and select interleaver bits. 📡
- **OFDM**: Define bandwidth, number of subcarriers, and other related parameters. 📶
- **Power Transmitted**: Input various gains, losses, and power levels to compute the transmitted power. ⚙️
- **Throughput**: Configure the system for throughput calculations based on different access methods. 🚀
- **Cellular System Design**: Calculate essential parameters for designing a cellular system. 📱

## Sample Calculations

### Sample Calculator Interface
<p align="center">
  <img src="https://github.com/user-attachments/assets/cbf4c20c-145d-4e07-923e-cd764e95ec1d" width="900">
</p>

### Sample Result
<p align="center">
  <img src="https://github.com/user-attachments/assets/fa9bdf7d-ffc8-4ca1-80d6-8783ff954765" width="600">
</p>



