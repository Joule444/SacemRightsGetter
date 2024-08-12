
def write_descriptions_to_file(descriptions, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for description in descriptions:
            f.write(description + '\n')