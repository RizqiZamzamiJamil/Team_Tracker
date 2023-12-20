import { registry } from "@web/core/registry"
const { Component } = team_tracker

export class TeamTrackerDashboard extends Component {}

TeamTrackerDashboard.template = "team_tracker.TeamTrackerDashboard"

registry.category("actions").add("team_tracker.team_tracker_board", TeamTrackerDashboard)

