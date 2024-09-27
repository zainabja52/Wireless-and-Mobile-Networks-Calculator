from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    calculation_type = data['type']
    if calculation_type == 'sampler_and_interleaver':
        return calculate_sampler_and_interleaver(data)
    elif calculation_type == 'ofdm':
        return calculate_ofdm(data)
    elif calculation_type == 'power_transmitted':
        return calculate_power_transmitted(data)
    elif calculation_type == 'throughput':
        return calculate_throughput(data)
    elif calculation_type == 'cellular_system':
        return calculate_cellular_system(data)
    else:
        return jsonify({"error": "Invalid calculation type"}), 400


def calculate_sampler_and_interleaver(data):
    try:
        bandwidth = float(data.get('bandwidth', 0))
        bandwidth_unit = data.get('bandwidth_unit', 'Hz')
        num_bits_per_sample = int(data['num_bits_per_sample'])
        compression_ratio = float(data['compression_ratio'])
        redundancy_ratio = float(data['redundancy_ratio'])
        interleaver_bits = int(data['interleaver_bits'])

        # Convert bandwidth based on selected unit
        if bandwidth_unit == 'kHz':
            bandwidth *= 1e3  # Convert kHz to Hz
        elif bandwidth_unit == 'MHz':
            bandwidth *= 1e6  # Convert MHz to Hz

        fs = 2 * bandwidth
        L = 2 ** num_bits_per_sample
        bit_rate_input = fs * num_bits_per_sample
        bit_rate_output = bit_rate_input * compression_ratio
        bit_rate_channel_encoder = bit_rate_output / redundancy_ratio
        interleaver_output = bit_rate_channel_encoder

        def format_k(value):
            return f"{(value / 1000) :.2f}k" if value >= 1000 else f"{value: :.2f}"

        results = {
            "Sampling Frequency (fs)": format_k(fs),
            "Number of Levels (L)": L,
            "Bit Rate at Input of Source Encoder": format_k(bit_rate_input),
            "Bit Rate at Output of Source Encoder": format_k(bit_rate_output),
            "Bit Rate at Output of Channel Encoder": format_k(bit_rate_channel_encoder),
            "Interleaver Bits": interleaver_bits,
            "Interleaver Output": format_k(interleaver_output)
        }

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def calculate_ofdm(data):
    try:
        bandwidth = float(data.get('bandwidth', 0))
        bandwidth_unit = data.get('bandwidth_unit', 'Hz')
        num_subcarriers = int(data.get('num_subcarriers', 1))
        num_subcarriers_unit = data.get('num_subcarriers_unit', 'Hz')
        num_symbols_per_rb = int(data.get('num_symbols_per_rb', 0))
        symbol_duration = float(data.get('symbol_duration', 1))  # Assume milliseconds as default
        symbol_duration_unit = data.get('symbol_duration_unit', 'ms')
        qam = int(data.get('qam', 1))
        num_parallel_rb = int(data.get('num_parallel_rb', 1))

        # Convert bandwidth to Hz if needed
        if bandwidth_unit == 'kHz':
            bandwidth *= 1e3
        elif bandwidth_unit == 'MHz':
            bandwidth *= 1e6

        if num_subcarriers_unit == 'kHz':
            num_subcarriers *= 1e3
        elif num_subcarriers_unit == 'MHz':
            num_subcarriers *= 1e6

        # Convert symbol duration to seconds
        if symbol_duration_unit == 'ms':
            symbol_duration /= 1000
        elif symbol_duration_unit == 'us':
            symbol_duration /= 1e6

        # Calculations
        bits_per_resource_element = math.log2(qam)
        bits_per_ofdm_symbol = bits_per_resource_element * (bandwidth / num_subcarriers)
        bits_per_ofdm_rb = bits_per_ofdm_symbol * num_symbols_per_rb
        maximum_transmission_rate = (num_parallel_rb * bits_per_ofdm_rb) / symbol_duration

        results = {
            "Bits per Resource Element": bits_per_resource_element,
            "Bits per OFDM Symbol": bits_per_ofdm_symbol,
            "Bits per OFDM Resource Block": bits_per_ofdm_rb,
            "Maximum Transmission Rate (bps)": maximum_transmission_rate
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def dbm_to_db(value_dbm):
    """Converts dBm to dB."""
    return value_dbm - 30  # Conversion formula dBm to dB


def get_float(value, default):
    try:
        return float(value) if value else default
    except ValueError:
        return default

def calculate_power_transmitted(data):
    try:
        # Constants
        K = -228.6 # Boltzmann constant in J/K
        # User inputs with proper error handling and default values
        Lp = get_float(data.get('Lp', 0), 0)
        Lp_unit = data.get('Lp_unit', 'dB')
        f = get_float(data.get('f', 1), 1)
        Gt = get_float(data.get('Gt', 0), 0)
        Gt_unit = data.get('Gt_unit', 'dB')
        Gr = get_float(data.get('Gr', 0), 0)
        Gr_unit = data.get('Gr_unit', 'dB')
        Lf = get_float(data.get('Lf', 0), 0)
        Lf_unit = data.get('Lf_unit', 'dB')
        R = get_float(data.get('R', 1), 1)  # Default rate
        R_unit = data.get('R_unit', 'bps')
        L0 = get_float(data.get('L0', 0), 0)
        L0_unit = data.get('L0_unit', 'dB')
        Ar = get_float(data.get('Ar', 0), 0)
        Ar_unit = data.get('Ar_unit', 'dB')
        At = get_float(data.get('At', 0), 0)
        At_unit = data.get('At_unit', 'dB')

        Nf = get_float(data.get('Nf', 0), 0)
        Nf_unit = data.get('Nf_unit', 'dB')

        T = get_float(data.get('T', 290), 290)  # Default temperature
        T_unit = data.get('T_unit', 'Kelvin')
        Fmargin = get_float(data.get('Fmargin', 0), 0)
        Fmargin_unit = data.get('Fmargin_unit', 'dB')
        M = get_float(data.get('M', 0), 0)
        M_unit = data.get('M_unit', 'dB')

        if 'modulation' not in data or 'ber_value' not in data:
            return jsonify({"error": "Missing 'modulation' or 'ber_value' data"}), 400
        modulation = data.get('modulation', 'BPSK/QPSK')
        ber_value = data.get('ber_value', '10^-4')

        if Lp_unit == 'dBm':
            Lp = dbm_to_db(Lp)
        if Gt_unit == 'dBm':
            Gt = dbm_to_db(Gt)
        if Gr_unit == 'dBm':
            Gr = dbm_to_db(Gr)
        if Lf_unit == 'dBm':
            Lf = dbm_to_db(Lf)
        if R_unit == 'kbps':
            R = R * 1000  # Convert kbps to bps
        elif R_unit == 'Mbps':
            R = R * 1000000  # Convert Mbps to bps
        elif R_unit == 'dBm':
            R = dbm_to_db(R)

        R = R  # Assume R is already in dB if not converted
        if R_unit in ['bps', 'kbps', 'Mbps']:  # Convert to dB only if R is not already in dB
            if R > 0:
                R = 10 * math.log10(R)

        if L0_unit == 'dBm':
            L0 = dbm_to_db(L0)

        if Ar_unit == 'dBm':
            Ar = dbm_to_db(Ar)
        if At_unit == 'dBm':
            At = dbm_to_db(At)
        if Nf_unit == 'dBm':
            Nf = dbm_to_db(Nf)
        if T_unit == 'Celsius':
            T = T + 273.15  # Convert Celsius to Kelvin
        elif T_unit == 'dBm':
            T = dbm_to_db(T)

        if T_unit in ['Kelvin', 'Celsius']:  # Convert to dB only if R is not already in dB
            if T > 0:
                T = 10 * math.log10(T)

        if Fmargin_unit == 'dBm':
            Fmargin = dbm_to_db(Fmargin)
        if M_unit == 'dBm':
            M = dbm_to_db(M)

        # BER table values based on modulation type and Eb/N0
        EbN0_dict = {
            'BPSK/QPSK': {
                "10^-1": 0, "10^-2": 4, "10^-3": 7, "10^-4": 8.3,  "10^-5": 9.5,  "10^-6": 10.6, "10^-7": 11.5, "10^-8": 12
            },
            '8-PSK': {
                "10^-1": 0, "10^-2": 6.5, "10^-3": 10, "10^-4": 12, "10^-5": 13.1, "10^-6": 14, "10^-7": 14.7,
                "10^-8": 15.2
            },
            '16-PSK': {
                "10^-1": 0, "10^-2": 11.1, "10^-3": 14.1, "10^-4": 16, "10^-5": 17.2, "10^-6": 18.1
            }
        }
        EbN0 = EbN0_dict[modulation][ber_value]

        # Calculations
        pr = M + K + T + Nf + R + EbN0  # Received power calculation corrected
        pt_dB = pr + Lp + Lf + L0 + Fmargin - Gt - Gr - Ar - At  # Transmitted power

        output_unit = data.get('output_unit', 'dB')  # Default to dB if not specified

        if output_unit == 'Watt':
            # Convert dB to Watts if requested
            pt_Watt = 10 ** (pt_dB / 10)
            pt = pt_Watt
            unit = 'Watts'
        else:
            # Otherwise, leave as dB
            pt = pt_dB
            unit = 'dB'

        results = {
            "Transmitted Power (Pt) [" + output_unit + "]": pt
        }
        return jsonify(results)
    except Exception as e:
        print(f"Error: {str(e)}")  # Log error for debugging
        return jsonify({"error": str(e)}), 400

def calculate_throughput(data):
    try:
        throughput = None
        # Data extraction with unit handling
        calculation_method = data['calculation_method']
        R_rate = float(data['R_rate'])
        R_rate_unit = data['R_rate_unit']
        tau = float(data['tau'])
        tau_unit = data['tau_unit']
        F_size = float(data['F_size'])
        F_size_unit = data['F_size_unit']
        f_rate = float(data['f_rate'])
        f_rate_unit = data['f_rate_unit']

        # Unit conversion for data rate
        if R_rate_unit == 'kbps':
            R_rate *= 1e3
        elif R_rate_unit == 'Mbps':
            R_rate *= 1e6

        # Unit conversion for time
        if tau_unit == 'us':
            tau *= 1e-6
        elif tau_unit == 'ms':
            tau *= 1e-3
        elif tau_unit == 's':
            tau *= 1.0

        # Unit conversion for frame size
        if F_size_unit == 'Kbits':
            F_size *= 1e3
        elif F_size_unit == 'Mbits':
            F_size *= 1e6

        # Unit conversion for frame rate
        if f_rate_unit == 'Kfps':
            f_rate *= 1e3
        elif f_rate_unit == 'Mfps':
            f_rate *= 1e6

        # Throughput calculations based on method selected
        if calculation_method == 'unslottednonpersistent':
            throughput = calculate_unslotted_nonpersistent(R_rate, tau, F_size, f_rate)
        elif calculation_method == 'slottednonpersistent':
            throughput = calculate_slotted_nonpersistent(R_rate, tau, F_size, f_rate)
        elif calculation_method == 'unslotted1persistent':
            throughput = calculate_unslotted_1persistent(R_rate, tau, F_size, f_rate)
        elif calculation_method == 'slotted1persistent':
            throughput = calculate_slotted_1persistent(R_rate, tau, F_size, f_rate)

        # Check if throughput was calculated
        if throughput is None:
         return jsonify({"error": "No valid calculation method found"}), 400
        # Return results as JSON
        throughput_percentage = throughput * 100
        results = {
            "Throughput (%)": f"{throughput_percentage:.2f}",
            "Throughput": f"{throughput:.2f}"
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def calculate_unslotted_nonpersistent(R_rate, tau, F_size, f_rate):

            T_frame = F_size / R_rate
            G = f_rate * T_frame
            alpha = tau / T_frame

            e_term = math.exp(-2 * alpha * T_frame)
            e_term1 = math.exp(-alpha * G)
            numerator = G * e_term
            denominator = G * (1 + 2 * alpha) + e_term1
            throughput = numerator / denominator
            throughput_percentage = throughput * 100
            return throughput

def calculate_slotted_nonpersistent(R_rate, tau, F_size, f_rate):
    T_frame = F_size / R_rate
    G = f_rate * T_frame
    alpha = tau / T_frame

    e_term = math.exp(-2 * alpha * T_frame)
    e_term1 = math.exp(-alpha * G)
    numerator = alpha * e_term
    denominator = (1 - e_term1 + alpha)
    throughput = numerator / denominator
    throughput_percentage = throughput * 100
    return throughput

def calculate_unslotted_1persistent(R_rate, tau, F_size, f_rate):

    T_frame = F_size / R_rate
    G = f_rate * T_frame
    alpha = tau / T_frame

    e_term = math.exp(-G * (2*alpha+1))
    e_term1 = math.exp(-alpha * G)
    e_term2 = math.exp(-G*(1+alpha))
    numerator = (G*(1+G+(G*alpha)*(1+G+(G*alpha)/2))*e_term)
    denominator = (G*(1+2*alpha)-(1- e_term1) +(1+alpha*G)*e_term2)
    throughput = numerator / denominator
    throughput_percentage = throughput * 100
    return throughput

def calculate_slotted_1persistent(R_rate, tau, F_size, f_rate):

    T_frame = F_size / R_rate
    G = f_rate * T_frame
    alpha = tau / T_frame

    e_term1 = math.exp(-alpha * G)
    e_term2 = math.exp(-G * (1 + alpha))
    numerator = (G*(1+alpha-e_term1)*e_term2)
    denominator = ((1+alpha)*(1-e_term1) + alpha*e_term2)
    throughput = numerator / denominator
    throughput_percentage = throughput * 100
    return throughput

def calculate_cellular_system(data):
    try:
        transmitted_power = float(data['transmitted_power'])  # in Watts
        path_loss_exponent = float(data['path_loss_exponent'])  # dimensionless
        frequency = float(data['frequency'])  # in Hz
        required_coverage = float(data['required_coverage'])  # in meters

        # Simplified model for cell radius calculation using free space path loss formula
        c = 3 * 10 ** 8  # Speed of light in m/s
        wavelength = c / frequency

        # Calculate cell radius using a simplified path loss model
        cell_radius = (transmitted_power / required_coverage) ** (1 / path_loss_exponent) * wavelength

        results = {
            "Cell Radius (meters)": cell_radius
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
