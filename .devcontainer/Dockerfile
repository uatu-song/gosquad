FROM node:20

ARG TZ
ENV TZ="$TZ"

# Install basic development tools, iptables/ipset for the firewall, and
# python3 (this repo ships Python tooling under _tools/).
RUN apt update && apt install -y less \
  git \
  procps \
  sudo \
  fzf \
  zsh \
  man-db \
  unzip \
  gnupg2 \
  gh \
  aggregate \
  iptables \
  ipset \
  iproute2 \
  dnsutils \
  jq \
  python3 \
  python3-pip \
  python3-venv

ENV DEVCONTAINER=true

# Persist bash history across container rebuilds.
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
  && mkdir /commandhistory \
  && touch /commandhistory/.bash_history \
  && chown -R node /commandhistory

# Create workspace and config directories and set ownership.
RUN mkdir -p /workspace /home/node/.claude && \
  chown -R node:node /workspace /home/node/.claude

WORKDIR /workspace

# Install git-delta for nicer diffs.
RUN ARCH=$(dpkg --print-architecture) && \
  wget -q "https://github.com/dandavison/delta/releases/download/0.18.2/git-delta_0.18.2_${ARCH}.deb" && \
  dpkg -i "git-delta_0.18.2_${ARCH}.deb" && \
  rm "git-delta_0.18.2_${ARCH}.deb"

# Drop to the non-root user for the rest of the setup.
USER node

# npm global install location on PATH.
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$PATH:/usr/local/share/npm-global/bin

ENV SHELL=/bin/zsh

# Install a zsh + fzf shell setup.
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
  -p git \
  -p fzf \
  -a "source /usr/share/doc/fzf/examples/key-bindings.zsh" \
  -a "source /usr/share/doc/fzf/examples/completion.zsh" \
  -a "export PROMPT_COMMAND='history -a'" \
  -a "export HISTFILE=/commandhistory/.bash_history" \
  -x

# Install Claude Code.
RUN npm install -g @anthropic-ai/claude-code

# Copy the firewall init script and allow the node user to run it via sudo.
COPY init-firewall.sh /usr/local/bin/
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh && \
  echo "node ALL=(root) NOPASSWD: /usr/local/bin/init-firewall.sh" > /etc/sudoers.d/node-firewall && \
  chmod 0440 /etc/sudoers.d/node-firewall
USER node
