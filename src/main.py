import ntcore
import time

if __name__ == "__main__":
  inst = ntcore.NetworkTableInstance.getDefault()
  table = inst.getTable("led")

  led_panel_pattern_sub = table.getStringTopic("ledPanelPattern").subscribe("")

  inst.startClient4("LIN Client")
  inst.setServerTeam(4546)

  while True:
    time.sleep(1)

    led_panel_pattern = led_panel_pattern_sub.get()
    print(f"LED Panel Pattern: {led_panel_pattern}")
    # make the panel actually do the pattern