from helpers import run_cli


def test_reads_more_than_200_reservations(tmp_path):
    """Garante que todas as reservas do CSV sejam processadas."""
    rows = [
        {"reservation_id": f"R-{i}"}
        for i in range(250)
    ]

    report = run_cli(tmp_path, rows)

    assert report["summary"]["total_reservations"] == 250