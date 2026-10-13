# Publishing

## Setup

1. Enable Fedora 43, 44, 45, and Rawhide for `x86_64` and `aarch64` in the [COPR project](https://copr.fedorainfracloud.org/coprs/g/uji-labs/Uji/).
   Keep build network access disabled.
2. Create the `copr` environment in [GitHub repository settings](https://github.com/uji-labs/copr/settings/environments).
   Restrict deployment branches to `master`.
3. Set the environment variable `COPR_TARGET` to `@uji-labs/Uji`.
4. Set the environment secret `COPR_CONFIG` to the complete configuration from your [COPR API page](https://copr.fedorainfracloud.org/api/).
   Include `[copr-cli]` and keep all values unchanged.

Do not put credentials in Git, logs, issues, or screenshots.

## Publish

1. Update the version, pinned source commit, release number, and changelog in `uji.spec`.
   Increase the release number when you change packaging for the same upstream version.
2. Review dependency licenses and merge into `master` after the package checks pass.
3. Open [Build Fedora packages](https://github.com/uji-labs/copr/actions/workflows/build.yml).
   Select **Run workflow**, choose `master`, and enable `submit_to_copr`.
4. Wait for GitHub checks and publication to finish.
   Open the COPR build link in the publication log and confirm that all eight targets succeed.
   Investigate failed or skipped targets before announcing the release.
5. Follow the [installation instructions](../README.md#installation) and check `uji --version` on Fedora.

Publication submits the Fedora 44 source package only after all GitHub build jobs pass.
Leave `submit_to_copr` disabled for checks without publication.

## Replace the API token

Replace the token before the expiration date shown on the COPR API page.

1. Wait for active publication jobs to finish.
2. Open your [COPR API page](https://copr.fedorainfracloud.org/api/) and select **Generate a new token**.
   The replacement invalidates the old token.
3. Copy the complete API configuration into the `COPR_CONFIG` environment secret in GitHub.
   Update other clients that use the same credentials.
4. Note the expiration date and test the credentials during your next intended publication.
   A run with publication disabled does not test COPR authentication.

If credentials leak, replace the token and update the secret immediately, even if publication jobs are active.
Deleting the GitHub secret does not revoke the COPR token.
