"""
This file transform the SQL produced by MySQL on SQL that can execute on PostgreSQL
"""


__READ_SQL_FILE__ = "original_schema_msql.sql"

__OUTPUT_SQL_FILE__ = "02_create_schema_db_for_postgresql.sql"


def replace_phrases(text):
    text = text.replace("mydb", "pauliceia")
    text = text.replace("`", "'")
    text = text.replace("TINYINT(1)", "BOOLEAN")
    text = text.replace("ENGINE = InnoDB", "")
    text = text.replace("ON DELETE NO ACTION", "ON DELETE CASCADE")
    text = text.replace("ON UPDATE NO ACTION", "ON UPDATE CASCADE")

    text = text.replace("""SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;""", "")
    text = text.replace("""SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';""", "")

    text = text.replace("-- MySQL Script generated by MySQL Workbench", "")
    text = text.replace("-- Model: New Model    Version: 1.0", "")
    text = text.replace("-- MySQL Workbench Forward Engineering", "")
            
    text = text.replace(")\n;", "\n);")  # put the ) and ; together, and in other line
    text = text.replace("'", "")
    text = text.replace("USE pauliceia ;", "")
    text = text.replace(" DEFAULT CHARACTER SET utf8", "")

    # if the geometries are not in text, so replace them
    if "GEOMETRY(MULTIPOINT, 4326)" not in text:
        text = text.replace("MULTIPOINT", "GEOMETRY(MULTIPOINT, 4326)")
    if "GEOMETRY(MULTILINESTRING, 4326)" not in text:
        text = text.replace("MULTILINESTRING", "GEOMETRY(MULTILINESTRING, 4326)")
    if "GEOMETRY(MULTIPOLYGON, 4326)" not in text:
        text = text.replace("MULTIPOLYGON", "GEOMETRY(MULTIPOLYGON, 4326)")

    return text

def remove_bad_lines_and_put_default_values(text):
        
    lines = text.split("\n")
    lines_copy = list(lines)  # create a copy to iterate inside it

    # iterate reversed
    for i in range(len(lines_copy)-1, -1, -1):
        line = lines_copy[i]
        
        line_lower = line.lower()

        # if there is a index line, so remove it in the original list
        if "index" in line_lower or ("brst" in line_lower and "2017" in line_lower):
            del lines[i]
            continue

        # put cascade in the final of line
        if ("drop schema if exists" in line_lower or "drop table if exists" in line_lower) \
            and "cascade" not in line_lower:
            lines[i] = lines[i].replace(";", "CASCADE ;")

        # put default values, but NOT in FKs
        if "visible boolean" in line_lower and "fk" not in line_lower:
            lines[i] = lines[i].replace(",", " DEFAULT TRUE,")

        if "version int" in line_lower and "fk" not in line_lower:
            lines[i] = lines[i].replace(",", " DEFAULT 1,")

        # default FALSE to "is_read" column, because is True, just if the user read the message
        if "is_read boolean" in line_lower:
            lines[i] = lines[i].replace(",", " DEFAULT FALSE,")

    text = "\n".join(lines)

    return text

def add_serial_number_in_ID(text):
    lines = text.split("\n")
    lines_copy = list(lines)  # create a copy to iterate inside it

    for i in range(0, len(lines_copy)):
        line = lines_copy[i]

        line_lower = line.lower()

        # put SERIAL just in ID field, NOT in FKs
        if "id int" in line_lower and "fk" not in line_lower:
            line_splited = line.replace("NOT NULL", "").split(" ")
            line_splited[3] = "SERIAL"                
            lines[i] = " ".join(line_splited)

    text = "\n".join(lines)

    return text

def arrange_table_auth(text):   
    lines = text.split("\n")
    lines_copy = list(lines)  # create a copy to iterate inside it

    for i in range(0, len(lines_copy)):
        line = lines_copy[i]

        line_lower = line.lower()

        # put default values to 'is_admin' and 'allow_import_bulk'
        if ("is_admin boolean" in line_lower) or ("allow_import_bulk boolean" in line_lower):
            lines[i] = lines[i].replace(",", " DEFAULT FALSE,")

    text = "\n".join(lines)

    return text

def last_modifications(text):

    # remove the schema
    text = text.replace("pauliceia.", "")

    text = text.replace("""
-- -----------------------------------------------------
-- Schema pauliceia
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS pauliceia CASCADE ;

-- -----------------------------------------------------
-- Schema pauliceia
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS pauliceia ;""", "")

    text = text.replace("\n\n\n\n", "\n")

    text = text.replace(" user ", " user_ ")

    return text


def main():
    """
    This function replace code from MySQL generate
    by MySQL Workbench to PostgreSQL SQL
    with some modifications to Pauliceia
    """

    with open(__OUTPUT_SQL_FILE__, 'a') as file_output, open(__READ_SQL_FILE__, 'r') as file_read:
        text = file_read.read() # read everything in the file
        

        text = replace_phrases(text)
        
        # remove bad lines     
        text = remove_bad_lines_and_put_default_values(text)

        # arrange table 'auth'
        text = arrange_table_auth(text)

        # add SERIAL number in ID
        text = add_serial_number_in_ID(text)

        text = last_modifications(text)


        # after all modification save it in file again
        
        file_output.seek(0) # rewind (return pointer to top of file)
        file_output.truncate() # clear file
        file_output.write(text) # write the updated text before

        print("All file was changed with sucess!")
       
main()
