# Required Arguments for VSTS
# - ROOTINSTALLDIR = the root directory for installation
# - RELEASE_RELEASEID = the release Id
# - AGENT_RELEASEDIRECTORY = the artifact directory for this release

if [ ! -d "$ROOTINSTALLDIR" ]; then
  mkdir $ROOTINSTALLDIR
fi
if [ ! -d "$ROOTINSTALLDIR/$RELEASE_RELEASEID" ]; then
  mkdir $ROOTINSTALLDIR/$RELEASE_RELEASEID
fi

# Copy files to the install dir:
cp -r $AGENT_RELEASEDIRECTORY $ROOTINSTALLDIR/$RELEASE_RELEASEID