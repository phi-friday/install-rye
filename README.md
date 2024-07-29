# install-rye

install [rye](https://github.com/astral-sh/rye) in github action

## how to use
```yaml
- uses: phi-friday/install-rye@v1.5
  id: install-rye
  with:
    rye_version: "latest" # optional
    rye_home: "" # optional
    python_version: 3.12 # optional
    use_uv: true # optional
```

### with cache
```yaml
strategy:
  fail-fast: true
  matrix:
    include:
      - rye_version: "0.37.0"
        rye_home: "/opt/rye"
        use_uv: "true"

steps:
  - uses: actions/cache@v4
    id: get-cache
    key: "${{ matrix.rye_version }}-${{ matrix.use_uv }}"
    path: "${{ matrix.rye_home }}"

  - uses: phi-friday/install-rye@v1.2
    if: steps.get-cache.outputs.cache-hit != 'true'
    id: install-rye
    with:
      rye_version: "${{ matrix.rye_version }}"
      rye_home: "${{ matrix.rye_home }}"
      use_uv: "${{ matrix.use_uv }}"
```

## output
1. `rye-version`

installed rye version.
> ex: `0.37.0`

2. `rye-home`

installed rye path
> ex: `/home/runner/.rye`

3. `python-version`

pinned python version
> ex: `3.12.4`

4. `use-uv`

use uv flag
> ex: `true`