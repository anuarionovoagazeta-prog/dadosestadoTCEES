name: Consolidar dados.json

on:
  push:
    paths:
      - '**/*.json'
  workflow_dispatch: {}

jobs:
  consolidate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Run consolidation script
        run: |
          python3 scripts/merge_dados.py

      - name: Commit results
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add dados.json || true
          if ! git diff --cached --quiet; then
            git commit -m "chore: gerar dados.json (automated)"
            git push
          else
            echo "No changes to commit"
          fi
