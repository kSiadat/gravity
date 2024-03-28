to run the program run display.py

for settings.py:
  win_size    pixel dimensions of window
  blobs       number of initial blobs (entities)
  radius      radius of each initial blob
  mass        mass of each initial blob
  range       radius of area for inital blobs' inital location
  gravity     multiplier for gravitational force strength
  sigma       standard deviation for intial blobs' intial velocity
  col_set     boolean to determine if you choose the blob/trail colour
  colour      blob/trail colour
  trail       boolean to determine if trails are visible
  trail_len   length of trails in frames
  shade       darkest rgb value as a single int, for random colours
  camera      choose inital type from: fixed (on origin) / largest (follow largest blob) / com (follow centre of mass) / adjust (manual movement)
  cam_move    keys for moving the camera in adjust mode
  cam_step    distance to move camera on each key press
  cam_typ     keys for setting camera type
