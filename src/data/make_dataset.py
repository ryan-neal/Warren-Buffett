# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
from scraper import scrape_buffett
from load_reports import load_data
from src.global_settings import DATA_DIR, DATA_RAW_DIR, VALID_REPORT_YEARS


@click.command()
@click.argument('input_filepath', default=DATA_RAW_DIR, type=click.Path(exists=True))
@click.argument('output_filepath', default=DATA_DIR, type=click.Path())
def main(input_filepath=None, output_filepath=None):
    """
    Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # check if data path exists
    if os.path.exists(DATA_RAW_DIR):
        file_list = os.listdir(DATA_RAW_DIR)

        # check if all the files are there
        file_list_joined = ','.join(file_list)

        missing = []
        for year in VALID_REPORT_YEARS:
            if str(year) not in file_list_joined:
                missing.append(year)

        if missing:
            missing_str = ", ".join(map(str, missing))
            logging.info('missing years: {}'.format(missing_str))
            logging.info('running buffet scraper')
            scrape_buffett()
        else:
            logger.info('data already exists. not running buffet scraper')
    else:
        logging.info("Path {} does not exist.".format(DATA_RAW_DIR))
        logging.info('running buffet scraper')
        scrape_buffett()

    logger.info('loading data into db')
    load_data()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
