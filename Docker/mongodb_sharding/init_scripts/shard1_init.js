host1 = process.env.MONGODB_SERVER + ':50001';
host2 = process.env.MONGODB_SERVER + ':50002';

rs.initiate(
    {
        _id: "shard1rs",
        members: [
            { _id: 0, host: host1 },
            { _id: 1, host: host2 },
        ]
    }
)