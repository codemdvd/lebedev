host1 = process.env.MONGODB_SERVER + ':50003';
host2 = process.env.MONGODB_SERVER + ':50004';

rs.initiate(
    {
        _id: "shard2rs",
        members: [
            { _id: 0, host: host1 },
            { _id: 1, host: host2 },
        ]
    }
)