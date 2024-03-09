# install-rye

install [rye](https://github.com/astral-sh/rye) in github action

## how to use
```yaml
- uses: phi-friday/install-rye@v1.1
  id: install-rye
  with:
    rye_version: "latest" # optional
    rye_home: "" # optional
    python_version: 3.12 # optional
    use_uv: true # optional
```

## output
1. `rye-version`

installed rye version.
> ex: `0.28.0`

2. `rye-home`

installed rye path
> ex: `/home/runner/.rye`

3. `python-version`

pinned python version
> ex: `3.12.2`

4. `use-uv`

use uv flag
> ex: `true`