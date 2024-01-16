import logging

import hydra


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@hydra.main(config_path="configs", config_name="cfg", version_base=None)
def main(cfg):

    from time import sleep

    import pandas as pd
    from sqlalchemy import create_engine

    log.info("Sleeping for 10 seconds to allow postgresql init...")
    sleep(10)

    log.info(f"Connection to the database: '{cfg.db.name}'...")
    db_address = (
        f"{cfg.db.type}://{cfg.db.user}:"
        f"{cfg.db.password}@{cfg.db.host}:"
        f"{cfg.db.port}/{cfg.db.name}"
    )
    engine = create_engine(db_address)
    log.info("Connection established!")

    log.info(f"Loading file '{cfg.data.filenames.users}' to the database...")
    df_users = pd.read_csv(cfg.data.dir_path + cfg.data.filenames.users)
    df_users.to_sql(
        name=cfg.db.tables.users, con=engine, index=False, if_exists="replace"
    )
    log.info("Successfully loaded!")

    log.info(f"Loading file '{cfg.data.filenames['items']}' to the database...")
    df_items = pd.read_csv(cfg.data.dir_path + cfg.data.filenames["items"])
    df_items.to_sql(
        name=cfg.db.tables["items"], con=engine, index=False, if_exists="replace"
    )
    log.info("Successfully loaded!")

    log.info(f"Loading file '{cfg.data.filenames.interactions}' to the database...")
    df_interactions = pd.read_csv(cfg.data.dir_path + cfg.data.filenames.interactions)
    df_interactions.to_sql(
        name=cfg.db.tables.interactions, con=engine, index=False, if_exists="replace"
    )
    log.info("Successfully loaded!")

    log.info(f"Loading file '{cfg.data.filenames.links}' to the database...")
    df_links = pd.read_csv(cfg.data.dir_path + cfg.data.filenames.links, sep="|")
    df_links.to_sql(
        name=cfg.db.tables.links, con=engine, index=False, if_exists="replace"
    )
    log.info("Successfully loaded!")


if __name__ == "__main__":
    main()
