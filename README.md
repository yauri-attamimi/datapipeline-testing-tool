<!--
title: 'datapipeline-testing-tool'
description: 'A container-based testing tool for bulking up our Data Pipeline with some data'
layout: Doc
framework: v3
platform: Docker
language: python
priority: 2
authorLink: 'https://github.com/yauritux'
authorName: 'Yauri Attamimi'
authorAvatar: 'https://avatars.githubusercontent.com/u/515690?s=400&u=c238ad162c1f444e80ebbefc243cfaf701f3420e&v=4'
-->

# Data Pipeline Testing Tool

A container-based testing tool for bulking up our `Data Pipeline` with some data.

## Usage

### Build testing data

Open up file `doc/DriverDailyMetrics.xlsx`, update the testing data as needed.

### Build the Image

```bash
$ docker build -t moove/datapipeline-testing-tool:latest .
```

### Starting to feed our `data-pipeline`

```bash
docker container run -d --rm moove/datapipeline-testing-tool:latest
```

Running the above command will automatically fetch all data from `doc/DriverDailyMetrics.xlsx` by default.
