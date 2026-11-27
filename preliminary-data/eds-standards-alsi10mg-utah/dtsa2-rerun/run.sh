#!/usr/bin/env bash
# Re-run DTSA-II's quantification of the caliber#35 spectra, headless. See README.md.
#
# Needs git, curl, Maven and Python 3 (standard library only). It downloads a JDK 26 and
# builds NIST's EPQ library (the engine inside DTSA-II) at a pinned commit, all in a
# temporary directory. Set JAVA26_HOME to use a JDK 26 you already have, and WORK to
# keep the build between runs.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW="$(cd "$HERE/../raw" && pwd)"
WORK="${WORK:-$(mktemp -d)}"
EPQ_COMMIT=249dd3f805545bae1e1b2254fd7fd1cd4dc3d8f2 # usnistgov/EPQ master, "Polaris" 2026-09-10
EPQ_VERSION=15.1.57

if [ -z "${JAVA26_HOME:-}" ]; then
  mkdir -p "$WORK/jdk"
  curl -fsSL "https://api.adoptium.net/v3/binary/latest/26/ga/linux/x64/jdk/hotspot/normal/eclipse" | tar xz -C "$WORK/jdk"
  JAVA26_HOME="$(ls -d "$WORK"/jdk/jdk-26*)"
fi
export JAVA_HOME="$JAVA26_HOME" PATH="$JAVA26_HOME/bin:$PATH"

if [ ! -f "$WORK/epq/target/epq-$EPQ_VERSION.jar" ]; then
  git init -q "$WORK/epq"
  git -C "$WORK/epq" fetch -q --depth 1 https://github.com/usnistgov/EPQ.git "$EPQ_COMMIT"
  git -C "$WORK/epq" checkout -q FETCH_HEAD
  (cd "$WORK/epq" &&
    sed -e "s/NUMBER_VERSION/$EPQ_VERSION/g" -e "s/JDK_VERSION/26/g" pom.template >pom.xml &&
    mvn -q -B -Dmaven.test.skip=true package &&
    mvn -q -B dependency:build-classpath -Dmdep.outputFile="$WORK/cp.txt")
fi
CP="$WORK/epq/target/epq-$EPQ_VERSION.jar:$(cat "$WORK/cp.txt")"

run() { # run <out dir> <config> [options]
  local out="$1"
  shift
  java --enable-preview --source 26 -Depq.version="${EPQ_COMMIT:0:7}" -cp "$CP" \
    "$HERE/RerunDTSA2.java" "$RAW" "$out" "$@" 2>&1 | grep -v -e '^WARNING' -e 'TACTYLR' || true
}

# 1. The student's entries, including the MgO spectrum entered as pure Mg in trials 11 and 14.
run "$HERE" as-entered --pure-mg-runs trial11_1,trial14_1
# 2. The same, with MgO entered as MgO everywhere.
run "$HERE" mgo
# 3. As 2, but the 0.96 us runs are fitted against standards broadened to their resolution
#    (135.5 eV at Mn Ka, the EDAX header value, which the peak widths confirm).
run "$HERE" broadened --broaden-to 135.5 --amp 0.96

# Checks on sobol_exp_1_1, the one clean run.
# a. Broaden the unknown alone, as a 0.96 us amp time would: does it look like the 11-18 runs?
run "$HERE/checks" unknown-broadened --runs sobol_exp_1_1 --unk-extra 44.45
# b. Broaden the unknown and the standards together: does 3's correction recover the native result?
run "$HERE/checks" both-broadened --runs sobol_exp_1_1 --broaden-to 135.5 --amp 7.68 --unk-extra 44.45
# c. How much does the detector resolution entered in DTSA-II move the result?
for fw in 120 135.5 145; do
  run "$HERE/checks" "detector-$fw" --runs sobol_exp_1_1,trial8_1,trial13_1 --fwhm "$fw"
done

python3 "$HERE/compare.py"
