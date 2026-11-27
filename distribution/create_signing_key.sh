#!/usr/bin/env bash
set -euo pipefail
umask 077
target="${1:?Supply a secure directory outside the repository}"
mkdir -p "$target"
target="$(cd "$target" && pwd -P)"
repo="$(cd "$(dirname "$0")/.." && pwd -P)"
case "$target/" in "$repo/"*) echo 'Refusing to store private key inside repository' >&2; exit 1;; esac
test ! -e "$target/valentina-private.pem"
test ! -e "$target/valentina-public.pem"
openssl genpkey -algorithm ED25519 -out "$target/valentina-private.pem"
openssl pkey -in "$target/valentina-private.pem" -pubout -out "$target/valentina-public.pem"
openssl pkey -pubin -in "$target/valentina-public.pem" -outform DER | openssl dgst -sha256
echo 'Keep the private PEM offline. Only the public PEM may be committed.'
