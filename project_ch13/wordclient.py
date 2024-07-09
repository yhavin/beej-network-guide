import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s: socket.socket):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    # TODO -- Write me!
    while len(packet_buffer) < WORD_LEN_SIZE:
        data = s.recv(1024)
        if not data:
            return None
        packet_buffer += data

    word_len = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], "big")
    packet_buffer = packet_buffer[WORD_LEN_SIZE:]

    while len(packet_buffer) < word_len:
        data = s.recv(1024)
        if not data:
            return None
        packet_buffer += data

    word_packet = packet_buffer[:word_len]
    packet_buffer = packet_buffer[word_len:]

    return word_packet
    


def extract_word(word_packet: bytes):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    # TODO -- Write me!
    return word_packet.decode("UTF-8")

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))