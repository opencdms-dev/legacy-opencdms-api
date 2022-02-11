required_role_lookup = {
    "/climsoft/v1/climsoft-users": {
        "post": {"ClimsoftAdmin"},
        "get": {"ClimsoftAdmin"},
        "put": {"ClimsoftAdmin"},
        "delete": {"ClimsoftAdmin"}
    },
    "/climsoft/v1/file-upload/image": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/s3/image": {
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"}
    },
    "/climsoft/v1/acquisition-types": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/data-forms": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/fault-resolutions": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/feature-geographical-positions": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/flags": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/instruments": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftOperator"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"}
    },
    "/climsoft/v1/instrument-fault-reports": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"}
    },
    "/climsoft/v1/instrument-inspections": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"}
    },
    "/climsoft/v1/obselements": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/observation-finals": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftOperator"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftOperator"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftOperator"}
    },
    "/climsoft/v1/observation-initials": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC", "ClimsoftOperator", "ClimsoftOperatorSupervisor"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC", "ClimsoftOperator", "ClimsoftOperatorSupervisor"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC", "ClimsoftOperator", "ClimsoftOperatorSupervisor"}
    },
    "/climsoft/v1/obs-schedule-class": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/paper-archives": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/paper-archive-definitions": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/physical-features": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/physical-feature-class": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/qc-status-definitions": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC"}
    },
    "/climsoft/v1/qc-types": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftQC"}
    },
    "/climsoft/v1/reg-keys": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    },
    "/climsoft/v1/stations": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"}
    },
    "/climsoft/v1/station-elements": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"}
    },
    "/climsoft/v1/station-location-histories": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"}
    },
    "/climsoft/v1/station-qualifiers": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata"}
    },
    "/climsoft/v1/synop-features": {
        "post": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "get": {"ClimsoftAdmin", "ClimsoftDeveloper", "ClimsoftMetadata", "ClimsoftOperator",
                "ClimsoftOperatorSupervisor", "ClimsoftProducts", "ClimsoftQC", "ClimsoftRainfall", "ClimsoftRainfall"},
        "put": {"ClimsoftAdmin", "ClimsoftDeveloper"},
        "delete": {"ClimsoftAdmin", "ClimsoftDeveloper"}
    }
}
