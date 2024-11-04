from app import auth_jwt_service, db, logger, loop, redis_client, server


if __name__ == "__main__":
    logger.info("Start server connections checking.")

    try:
        auth_jwt_service._set_keys()
        logger.info("Success load jwt keys.")
    except Exception as err:
        logger.error(f"Failed load jwt keys, reason: {err}")
        exit(0)

    try:
        db.session.connection()
        logger.info("Success connect to database")
    except Exception as err:
        logger.error(f"Failed connect to database, reason: {err}")
        exit(0)

    try:
        redis_client.ping()
        logger.info("Success connect to redis")
    except Exception as err:
        logger.error(f"Failed connect to Redis, reason: {err}")
        exit(0)

    loop.create_task(server.serve())

    try:
        logger.info("Server started.")
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Server prevent stopped.")
    except BaseException as err:
        logger.critical(f"Server prevent stopped. Error: {err}")
