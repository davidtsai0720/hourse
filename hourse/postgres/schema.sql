CREATE TABLE IF NOT EXISTS city(
    id BIGSERIAL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY(id),
    CONSTRAINT city_name_unique UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS section(
    id BIGSERIAL,
    city_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY(id),
    CONSTRAINT section_name_city_id_unique UNIQUE(name, city_id),
    CONSTRAINT section_city_id_foreign FOREIGN KEY (city_id) REFERENCES city(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS hourse(
    id BIGSERIAL,
    section_id INTEGER NOT NULL,
    link VARCHAR(125) NOT NULL,
    layout VARCHAR(32),
    address VARCHAR(64),
    price DECIMAL(8, 2) NOT NULL,
    current_floor VARCHAR(8) NOT NULL,
    total_floor VARCHAR(8) NOT NULL,
    shape VARCHAR(16) NOT NULL,
    age VARCHAR(16) NOT NULL,
    area DECIMAL(8, 2) NOT NULL,
    main_area DECIMAL(8, 2),
    commit VARCHAR(255),
    raw jsonb NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY(id),
    CONSTRAINT hourse_link_unique UNIQUE(link),
    CONSTRAINT hourse_section_id_foreign FOREIGN KEY (section_id) REFERENCES section(id) ON UPDATE CASCADE ON DELETE CASCADE
);
