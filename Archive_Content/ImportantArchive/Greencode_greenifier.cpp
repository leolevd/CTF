#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static constexpr const char* GREEN_COLOR = "\x1b[32m";
static constexpr const char* RESET_COLOR = "\x1b[0m";

void print_help(const std::string& program_name) {
    std::cout << "Usage: " << program_name << " [options] [text]\n"
              << "Options:\n"
              << "  -h, --help       Show this help message\n"
              << "  -f, --file FILE  Read input text from FILE\n"
              << "  -s, --seed TEXT  Seed the green transformation with TEXT\n"
              << "If text is provided as a positional argument, it will be greenified.\n";
}

std::string replace_word(std::string word) {
    static const std::vector<std::pair<std::string, std::string>> replacements = {
        {"red", "green"},
        {"brown", "leafy"},
        {"dirty", "fresh"},
        {"polluted", "pure"},
        {"dry", "lush"},
        {"dead", "alive"},
        {"dark", "emerald"},
        {"sad", "hopeful"},
        {"hot", "cool"},
        {"gray", "verdant"},
    };

    std::string lowercase = word;
    std::transform(lowercase.begin(), lowercase.end(), lowercase.begin(), [](unsigned char c) {
        return static_cast<char>(std::tolower(c));
    });

    for (const auto& pr : replacements) {
        if (lowercase == pr.first) {
            return pr.second;
        }
    }

    return word;
}

std::string greenify_text(const std::string& input) {
    std::istringstream tokenizer(input);
    std::ostringstream output;
    std::string token;
    bool first = true;

    while (tokenizer >> token) {
        std::string clean_word;
        std::string suffix;

        for (char c : token) {
            if (std::isalpha(static_cast<unsigned char>(c))) {
                clean_word += c;
            } else {
                suffix += c;
            }
        }

        std::string transformed = replace_word(clean_word);
        if (!first) {
            output << ' ';
        }
        first = false;
        output << transformed << suffix;
    }

    std::string result = output.str();
    if (!result.empty()) {
        result += " |Greenified|";
    }
    return result;
}

std::string read_file_contents(const std::string& path) {
    std::ifstream file(path);
    if (!file) {
        throw std::runtime_error("Unable to open file: " + path);
    }

    std::ostringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

int main(int argc, char* argv[]) {
    std::string program_name = argc > 0 ? argv[0] : "greenifier";
    std::string text;
    std::string file_path;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "-h" || arg == "--help") {
            print_help(program_name);
            return 0;
        }
        if (arg == "-f" || arg == "--file") {
            if (i + 1 >= argc) {
                std::cerr << "Error: missing file path after " << arg << "\n";
                return 1;
            }
            file_path = argv[++i];
            continue;
        }
        if (arg == "-s" || arg == "--seed") {
            if (i + 1 >= argc) {
                std::cerr << "Error: missing seed text after " << arg << "\n";
                return 1;
            }
            text = argv[++i];
            continue;
        }
        if (!text.empty()) {
            text += ' ';
        }
        text += arg;
    }

    try {
        if (!file_path.empty()) {
            text = read_file_contents(file_path);
        }

        if (text.empty()) {
            std::cout << "Enter text to greenify: ";
            std::getline(std::cin, text);
        }

        std::string greenified = greenify_text(text);
        std::cout << GREEN_COLOR << greenified << RESET_COLOR << "\n";
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << "\n";
        return 1;
    }

    return 0;
}
