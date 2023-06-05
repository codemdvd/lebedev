host1 = process.env.MONGODB_SERVER + ':40001';
host2 = process.env.MONGODB_SERVER + ':40002';
rs.initiate(
    {
        _id: "cfgrs",
        configsvr: true,
        members: [
            { _id : 0, host : host1 },
            { _id : 1, host : host2 }
        ]
    }
);
