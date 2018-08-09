# Required Arguments for VSTS
# - ROOTINSTALLDIR = the root directory for installation
# - RELEASE_RELEASEID = the release Id
# - ARTIFACTLOCATION = the artifact directory for this release

if [ ! -d "$ROOTINSTALLDIR" ]; then
  mkdir $ROOTINSTALLDIR
fi
if [ ! -d "$ROOTINSTALLDIR/$RELEASE_RELEASEID" ]; then
  mkdir $ROOTINSTALLDIR/$RELEASE_RELEASEID
fi

# Copy files to the install dir:
cp -r $ARTIFACTLOCATION $ROOTINSTALLDIR/$RELEASE_RELEASEID

# Create an images directory for the training photos
mkdir $ROOTINSTALLDIR/$RELEASE_RELEASEID/azure-custom-vision/images