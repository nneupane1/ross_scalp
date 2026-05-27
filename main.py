from core.event_loop import main_loop


def main() -> None:
    main_loop(poll_seconds=5)


if __name__ == "__main__":
    main()
