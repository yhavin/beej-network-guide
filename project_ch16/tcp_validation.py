import os


def main():
    for i in range(10):
        # Convert IP addresses to bytestrings
        text_file = open(os.path.join("project_ch16", f"tcp_addrs_{i}.txt"), "r")
        ip_addresses = text_file.readline().strip()
        text_file.close()
        source_ip, destination_ip = ip_addresses.split(" ")
        source_ip_bytes, destination_ip_bytes = convert_ip_to_bytestring(source_ip), convert_ip_to_bytestring(destination_ip)

        # Get TCP data length
        tcp_file = open(os.path.join("project_ch16", f"tcp_data_{i}.dat"), "rb")
        tcp_data = tcp_file.read()
        tcp_file.close()
        tcp_length = len(tcp_data)

        # Create IP pseudo header
        pseudo_header = source_ip_bytes + destination_ip_bytes + b"\x00" + b"\x06" + tcp_length.to_bytes(2, "big")

        # Extract actual TCP checksum
        tcp_checksum = int.from_bytes(tcp_data[16:18], "big")

        # Create zero-checksum TCP data
        tcp_data_zero_checksum = tcp_data[:16] + b"\x00\x00" + tcp_data[18:]

        # Right-zero-pad zero-checksum TCP data if odd length
        if len(tcp_data_zero_checksum) % 2 == 1:
            tcp_data_zero_checksum += b"\x00"

        # Concatenate pseudo header and zero-checksum TCP data
        data = pseudo_header + tcp_data_zero_checksum

        # Compute checksum
        checksum = compute_checksum(data)

        # Compare checksums
        if checksum == tcp_checksum:
            print("PASS")
        else:
            print("FAIL")


def convert_ip_to_bytestring(ip_address: str):
    integers = ip_address.split(".")
    bytestring = b"".join(int(integer).to_bytes(1, "big") for integer in integers)
    return bytestring


def compute_checksum(data: bytes):
    offset = 0
    total = 0

    while offset < len(data):
        word = int.from_bytes(data[offset:offset + 2], "big")  # 2-byte slice
        total += word
        total = (total & 0xffff) + (total >> 16)

        offset += 2  # Iterate through data in 2-byte steps

    # One's complement the sum
    total = (~total) & 0xffff

    return total


main()