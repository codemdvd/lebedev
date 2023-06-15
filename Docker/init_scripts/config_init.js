rs.initiate(
    {
        _id: "cfgrs",
        configsvr: true,
        members: [
            { _id : 0, host : 'cfgsvr1' },
            { _id : 1, host : 'cfgsvr2' }
        ]
    }
);
