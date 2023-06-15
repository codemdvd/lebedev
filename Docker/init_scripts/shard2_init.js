rs.initiate(
    {
        _id: "shard2rs",
        members: [
            { _id: 0, host: 'shard2svr1' },
            { _id: 1, host: 'shard2svr2' },
        ]
    }
);